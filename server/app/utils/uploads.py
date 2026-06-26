"""上传文件 URL 工具：统一生成与修正对外可访问的图片地址。"""


def build_upload_url(base_url: str, rel_path: str) -> str:
    """rel_path 形如 xhs/xxx.jpg，返回 {base}/uploads/xhs/xxx.jpg"""
    base = (base_url or '').rstrip('/')
    rel = rel_path.lstrip('/')
    return f'{base}/uploads/{rel}'


def normalize_upload_url(url: str, base_url: str) -> str:
    """将历史 localhost/127.0.0.1 等地址统一为配置的 PUBLIC_BASE_URL。"""
    if not url or '/uploads/' not in url:
        return url
    rel = url.split('/uploads/', 1)[1]
    return build_upload_url(base_url, rel)
