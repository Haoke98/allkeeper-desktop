# _*_ codign:utf8 _*_
import subprocess
import json
import logging

logger = logging.getLogger(__name__)

BROWSER_MAP = {
    'chrome': 'Google Chrome',
    'edge': 'Microsoft Edge',
    'safari': 'Safari',
    'opera': 'Opera',
    'firefox': 'Firefox',
    'brave': 'Brave Browser'
}

BROWSER_BUNDLE_IDS = {
    'chrome': 'com.google.Chrome',
    'edge': 'com.microsoft.edgemac',
    'safari': 'com.apple.Safari',
    'opera': 'com.operasoftware.Opera',
    'firefox': 'org.mozilla.firefox',
    'brave': 'com.brave.Browser'
}

class BrowserControlError(Exception):
    pass

class PermissionError(BrowserControlError):
    pass

def is_browser_installed(browser_key):
    bundle_id = BROWSER_BUNDLE_IDS.get(browser_key)
    if not bundle_id:
        return False
    
    # Safari is always installed on macOS
    if browser_key == 'safari':
        return True

    try:
        # mdfind is faster than checking paths recursively, but checking specific paths is fastest
        # However, apps can be anywhere. mdfind with bundle ID is robust.
        result = subprocess.run(
            ['mdfind', f"kMDItemCFBundleIdentifier == '{bundle_id}'"],
            capture_output=True,
            text=True,
            check=True
        )
        return bool(result.stdout.strip())
    except subprocess.SubprocessError:
        return False

def _run_applescript(script):
    try:
        # Run osascript with timeout to avoid hanging
        result = subprocess.run(
            ['osascript', '-e', script], 
            capture_output=True, 
            text=True, 
            check=True,
            timeout=5
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        logger.error("AppleScript execution timed out")
        raise BrowserControlError("Execution timed out")
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip()
        logger.error(f"AppleScript error: {error_msg}")
        if "-1743" in error_msg or "-10004" in error_msg or "权限违例" in error_msg or "privilege violation" in error_msg.lower():
            raise PermissionError("Permission denied. Please grant automation permission in System Preferences > Security & Privacy.")
        raise BrowserControlError(f"Script execution failed: {error_msg}")
    except Exception as e:
        logger.error(f"Unexpected error running AppleScript: {e}")
        raise BrowserControlError(str(e))

def get_browser_windows(browser_key):
    """
    Get list of open windows for the specified browser.
    Returns: [{'id': 123, 'title': 'Tab Title'}, ...]
    """
    app_name = BROWSER_MAP.get(browser_key)
    if not app_name:
        return []

    if browser_key == 'firefox':
        # Firefox AppleScript support is limited for window enumeration
        return []

    # Construct AppleScript to return JSON string
    script = ""
    if browser_key == 'safari':
        script = f'''
        tell application "{app_name}"
            set output to "["
            if running then
                repeat with w in windows
                    try
                        set win_id to id of w
                        set win_title to name of current tab of w
                        
                        -- Escape double quotes in title
                        set AppleScript's text item delimiters to "\\""
                        set textItems to text items of win_title
                        set AppleScript's text item delimiters to "\\\\\\""
                        set win_title to textItems as text
                        set AppleScript's text item delimiters to ""
                        
                        set output to output & "{{\\"id\\": " & win_id & ", \\"title\\": \\"" & win_title & "\\"}}::"
                    end try
                end repeat
            end if
            return output
        end tell
        '''
    else:  # Chromium based (Chrome, Edge, Opera, Brave)
        script = f'''
        tell application "{app_name}"
            set output to "["
            if running then
                repeat with w in windows
                    try
                        set win_id to id of w
                        set win_title to title of active tab of w
                        
                        -- Escape double quotes in title
                        set AppleScript's text item delimiters to "\\""
                        set textItems to text items of win_title
                        set AppleScript's text item delimiters to "\\\\\\""
                        set win_title to textItems as text
                        set AppleScript's text item delimiters to ""
                        
                        set output to output & "{{\\"id\\": " & win_id & ", \\"title\\": \\"" & win_title & "\\"}}::"
                    end try
                end repeat
            end if
            return output
        end tell
        '''

    try:
        output = _run_applescript(script)
    except PermissionError:
        # Re-raise permission error to be handled by caller
        raise
    except BrowserControlError:
        return []

    if not output or output == '[':
        return []

    windows = []
    # Parse our custom separated JSON objects
    # Output format: [{{...}}::{{...}}::
    try:
        parts = output.strip('[').split('::')
        for part in parts:
            if part.strip():
                # Replace any remaining newlines to avoid JSON errors
                clean_json = part.replace('\n', ' ').strip()
                windows.append(json.loads(clean_json))
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse window list JSON: {e}, output: {output}")
        return []
    
    return windows

def open_url(browser_key, url, window_id=None):
    """
    Open URL in specified browser and window.
    window_id: None/'new' for new window, or specific ID.
    """
    app_name = BROWSER_MAP.get(browser_key)
    if not app_name:
        return False, "Unknown browser"

    script = ""
    
    # 1. Open in NEW WINDOW
    if window_id == 'new' or not window_id:
        if browser_key == 'safari':
            script = f'''
            tell application "{app_name}"
                make new document with properties {{URL: "{url}"}}
                activate
            end tell
            '''
        elif browser_key == 'firefox':
             # For Firefox new window, simpler to use subprocess directly
             try:
                 subprocess.Popen(['open', '-a', app_name, '-n', '--args', '-new-window', url])
                 return True, "Opened in new window (Firefox)"
             except Exception as e:
                 return False, str(e)
        else: # Chromium based
            script = f'''
            tell application "{app_name}"
                make new window
                set URL of active tab of front window to "{url}"
                activate
            end tell
            '''
    
    # 2. Open in SPECIFIC WINDOW (Existing Process)
    else:
        try:
            win_id = int(window_id)
        except ValueError:
            return False, "Invalid window ID"

        if browser_key == 'safari':
            script = f'''
            tell application "{app_name}"
                tell window id {win_id}
                    make new tab with properties {{URL: "{url}"}}
                    set current tab to last tab
                end tell
                activate
            end tell
            '''
        elif browser_key == 'firefox':
            # Firefox doesn't support targeting windows by ID via AppleScript easily
            # Fallback to default open
            script = f'''
            tell application "{app_name}"
                open location "{url}"
                activate
            end tell
            '''
        else: # Chromium based
            script = f'''
            tell application "{app_name}"
                if running then
                    tell window id {win_id}
                        make new tab with properties {{URL: "{url}"}}
                    end tell
                    activate
                else
                    -- If not running, start it
                    activate
                    open location "{url}"
                end if
            end tell
            '''

    try:
        result = _run_applescript(script)
        return True, "Success"
    except PermissionError:
        return False, "Permission denied. Please check System Preferences > Security & Privacy > Automation."
    except BrowserControlError as e:
        # Fallback for Firefox new window handled above, but for others:
        if browser_key == 'firefox' and window_id == 'new':
             pass # Already handled
        return False, str(e)
