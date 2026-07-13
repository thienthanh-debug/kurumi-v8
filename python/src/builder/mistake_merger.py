import re

from src.ai.gemini_client import GeminiClient
from src.core.vault_reader import VaultReader


def resolve_full_content(vault: VaultReader, note_path: str) -> str:
    """
    Đọc 1 note. Nếu note chỉ là link trỏ sang ADR (vd chứa chữ 'ADR-014'),
    tự động tìm và đọc luôn nội dung ADR đó, ghép vào.
    Không để Gemini tự đoán nội dung từ cái tên link.
    """
    content = vault.read_note(note_path)

    # Tìm mọi cụm dạng ADR-XXX trong nội dung note
    adr_refs = re.findall(r"ADR-\d{3}", content)

    if not adr_refs:
        return content

    full_content = content
    for adr_id in set(adr_refs):
        matches = vault.find_notes_by_keyword(adr_id)
        if not matches:
            full_content += f"\n\n[CANH BAO: khong tim thay file cho {adr_id}]"
            continue
        adr_note = matches[0]
        adr_content = vault.read_note(adr_note)
        full_content += f"\n\n--- NOI DUNG DAY DU TU {adr_id} ({adr_note}) ---\n{adr_content}"

    return full_content


def merge_mistakes():
    vault = VaultReader()
    ai = GeminiClient()

    files = vault.find_notes_by_keyword("Mistake")
    files = [f for f in files if "MERGED" not in f]  # bo qua file gop cu neu co
    print(f"Tim thay {len(files)} file Mistake:")
    for f in files:
        print(f"  - {f}")

    combined = ""
    for f in files:
        full = resolve_full_content(vault, f)
        combined += f"\n\n===== FILE: {f} =====\n{full}"

    prompt = f"""Dưới đây là toàn bộ {len(files)} ghi chú "Mistake" trong dự án.
Một số ghi chú chỉ là link ngắn trỏ sang ADR — nội dung ĐẦY ĐỦ của ADR đó
đã được đính kèm ngay sau link, hãy dùng đúng nội dung đó, KHÔNG tự đoán
ý nghĩa chỉ từ cái tên file.
{combined}

Hãy làm 3 việc:
1. Nhóm các ghi chú có nội dung TRÙNG hoặc RẤT GIỐNG nhau lại với nhau (nêu rõ tên file nào thuộc nhóm nào).
2. Với mỗi nhóm trùng, viết lại thành MỘT bài học duy nhất, đầy đủ nhất, dựa ĐÚNG trên nội dung ADR đã đính kèm, không thuật ngữ kỹ thuật phức tạp.
3. Với ghi chú nào KHÔNG trùng với cái nào khác, giữ nguyên, chỉ viết lại cho dễ hiểu.

Trình bày kết quả rõ ràng theo từng mục, có tiêu đề."""

    print("\nDang nho Gemini phan tich va gop (co doc them ADR)...\n")
    result = ai.ask(prompt)

    output_path = vault.vault_path / "08-REFLECTION" / "Mistakes" / "Mistake-MERGED-DRAFT.md"
    output_path.write_text(result, encoding="utf-8")

    print(f"Da luu ban gop nhap tai: {output_path}")
    print("File goc CHUA bi xoa. Thanh tu xem va xoa file cu neu ung y.")


if __name__ == "__main__":
    merge_mistakes()