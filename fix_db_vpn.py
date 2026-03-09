import re

files = ["service/jumpService/models/services/db.py", "service/jumpService/models/services/vpn.py"]

for file_path in files:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # DbServiceUser remnant
    bad_block_db = '''class Meta:
        verbose_name = "数据库用户"
        verbose_name_plural = f"所有{verbose_name}"

    def __str__(self):
        return f"用户（{self.service.server.ip},{self.owner}）"'''
    
    # VPNUser remnant
    bad_block_vpn = '''class Meta:
        verbose_name = "VPN用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return f"VPN用户({self.username}@{self.service})"'''

    if file_path.endswith("db.py"):
        content = content.replace(bad_block_db, "")
    else:
        content = content.replace(bad_block_vpn, "")
    
    content = re.sub(r"\n\s*\n\s*\n", "\n\n", content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
