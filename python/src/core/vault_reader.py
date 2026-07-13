from pathlib import Path


class VaultReader:
    """
    Điểm chạm DUY NHẤT để đọc Obsidian vault Kurumi_V8.
    Vault chỉ là thư mục chứa file .md — không cần thư viện đặc biệt.
    """

    def __init__(self, vault_path: str = None):
        if vault_path is None:
            # Mặc định: vault nằm ngang hàng với thư mục python/
            vault_path = Path(__file__).resolve().parents[3]
        self.vault_path = Path(vault_path)

        if not self.vault_path.exists():
            raise FileNotFoundError(f"Khong tim thay vault tai: {self.vault_path}")

    def list_notes(self, subfolder: str = "") -> list[str]:
        """Liệt kê toàn bộ file .md trong vault (hoặc trong 1 thư mục con)."""
        search_path = self.vault_path / subfolder
        return [str(p.relative_to(self.vault_path)) for p in search_path.rglob("*.md")]

    def read_note(self, relative_path: str) -> str:
        """Đọc nội dung 1 file .md, theo đường dẫn tương đối trong vault."""
        file_path = self.vault_path / relative_path
        if not file_path.exists():
            raise FileNotFoundError(f"Khong tim thay note: {relative_path}")
        return file_path.read_text(encoding="utf-8")

    def find_notes_by_keyword(self, keyword: str) -> list[str]:
        """Tìm file .md có tên chứa từ khóa (không phân biệt hoa thường)."""
        keyword = keyword.lower()
        return [
            str(p.relative_to(self.vault_path))
            for p in self.vault_path.rglob("*.md")
            if keyword in p.name.lower()
        ]