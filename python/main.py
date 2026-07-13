from src.ai.gemini_client import GeminiClient
from src.core.vault_reader import VaultReader


def main():
    vault = VaultReader()
    ai = GeminiClient()

    print("=== KURUMI VAULT ASSISTANT ===")
    print("Go tu khoa de tim, hoac 'thoat' de dung.\n")

    while True:
        keyword = input("Tim ghi chu ve chu de gi? > ").strip()

        if keyword.lower() in ("thoat", "exit", "quit"):
            print("Tam biet.")
            break

        matches = vault.find_notes_by_keyword(keyword)

        if not matches:
            print(f"Khong tim thay ghi chu nao co ten chua '{keyword}'.\n")
            continue

        print(f"\nTim thay {len(matches)} ghi chu:")
        for i, name in enumerate(matches, 1):
            print(f"  {i}. {name}")

        choice = input("\nChon so de tom tat (hoac Enter de bo qua) > ").strip()

        if not choice:
            print()
            continue

        try:
            index = int(choice) - 1
            selected_note = matches[index]
        except (ValueError, IndexError):
            print("So khong hop le.\n")
            continue

        content = vault.read_note(selected_note)

        prompt = f"""Đây là nội dung ghi chú '{selected_note}':

{content}

Hãy tóm tắt ngắn gọn, dễ hiểu, không dùng thuật ngữ kỹ thuật phức tạp."""

        print("\nDang tom tat...\n")
        summary = ai.ask(prompt)
        print(f"===== TOM TAT: {selected_note} =====")
        print(summary)
        print()


if __name__ == "__main__":
    main()