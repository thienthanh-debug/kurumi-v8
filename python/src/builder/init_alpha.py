import os

# Đường dẫn vật lý đến Vault
VAULT_ROOT = r"D:\kurumi\Kurumi_V8"
PROJECT_DIR = os.path.join(VAULT_ROOT, "09-PROJECTS", "Inventory Refactoring Project Alpha")

# Kỷ luật: Chỉ tạo đúng những thứ Reality đang yêu cầu (Phase 0 và Khung Phase 1)
FILES_TO_CREATE = {
    "00-Mission.md": "# 🎯 MISSION\n**Dự án:** Inventory Refactoring Project Alpha\n**Mục tiêu:** Tách Human Workspace khỏi System Engine.\n**Trigger:** Reality báo cáo staff nhập liệu lag trên điện thoại.",
    "01-Reality_and_Domain.md": "# 👁️ PHASE 0 & 1: REALITY & DOMAIN\n\n## 1. Pain Points (Reality)\n- Staff nhập liệu lag trên điện thoại.\n- Prep Log lưu quá nhiều ngày.\n\n## 2. Business Events (Domain)\n*(Liệt kê các thao tác nhà hàng sinh ra dữ liệu tại đây...)*\n- Receive (Nhập hàng)\n- Prep (Sơ chế)\n- Waste (Hư hỏng)\n"
}

def scaffold_strictly():
    print("🚀 Khởi tạo Inventory Refactoring Project Alpha (Strict Mode)...")
    
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"📁 Đã chốt thư mục: {PROJECT_DIR}")

    for filename, content in FILES_TO_CREATE.items():
        filepath = os.path.join(PROJECT_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ Đã tạo file: {filename}")
        else:
            print(f"  ⚠️ File đã tồn tại: {filename}")

    print("\n🎉 Xong! Reality đã có chỗ để lên tiếng. Mời ní vào Obsidian.")

if __name__ == "__main__":
    scaffold_strictly()