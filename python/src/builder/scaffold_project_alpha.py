import os

# Đường dẫn gốc tới Vault (Ní nhớ đổi lại đường dẫn thật trên máy ní nha, ví dụ: D:\kurumi\Kurumi_V8)
VAULT_ROOT = r"D:\kurumi\Kurumi_V8"
PROJECT_DIR = os.path.join(VAULT_ROOT, "09-PROJECTS", "Inventory Refactoring Project Alpha")

# Danh sách các file cần tạo và nội dung nháp sẵn (Boilerplate)
FILES_TO_CREATE = {
    "00-Mission.md": "# 🎯 MISSION\n**Dự án:** Inventory Refactoring Project Alpha\n**Mục tiêu:** Tách Human Workspace khỏi System Engine.\n**Trigger:** Reality báo cáo staff nhập liệu lag trên điện thoại do gộp chung trách nhiệm Data Store và Workspace.",
    "01-Reality.md": "# 👁️ PHASE 0: REALITY RESEARCH\n## 1. Pain Points\n- Staff nhập liệu lag trên điện thoại.\n- Prep Log lưu quá nhiều ngày (không dọn dẹp).\n## 2. Current Architecture (As-Is)\n- Workspace và Data Store đang bị trộn lẫn (Mixed Responsibility).",
    "02-Domain.md": "# 🧠 PHASE 1: DOMAIN DISCOVERY\n## 1. Các khái niệm cốt lõi\n- **Workspace:** Nơi Human nhập liệu. Sống bao lâu? Khi nào dọn?\n- **Business Event:** Sự kiện kinh doanh cốt lõi (Prep, Waste, Receive).\n- **Ledger:** Nơi lưu trữ lịch sử vĩnh viễn.",
    "03-Architecture.md": "# 🏛️ PHASE 2: ARCHITECTURE DESIGN\n## Target Architecture (To-Be)\n- **Tầng 1:** Human Workspace (24h)\n- **Tầng 2:** Workflow (Review/Approval)\n- **Tầng 3:** Ledger (Immutable History)\n- **Tầng 4:** Engine (Calculation)\n- **Tầng 5:** Report",
    "04-Migration.md": "# 🔄 PHASE 3: MIGRATION PLAN\n## Chiến lược chuyển đổi (Từ As-Is sang To-Be)\n| Old Sheet | New Sheet | Dữ liệu mang theo | Rollback Plan |",
    "05-Implementation.md": "# ⚙️ PHASE 5: IMPLEMENTATION\n## Phân công (The Team)\n- **GPT:** Architecture Review & Domain Design\n- **Claude:** Code Apps Script, Boundary & State Machine\n- **Gemini:** Automation, Integration & Reflection\n- **Thanh:** Reality Testing & Approval",
    "06-Testing.md": "# 🧪 PHASE 4/6: TESTING & SIMULATION\n## Kịch bản Test\n- **Test 1:** Xóa/Clear Workspace -> Kiểm tra xem Ledger có bị mất data không?\n- **Test 2:** Submit 100 dòng sự kiện -> Đo tốc độ ghi.",
    "07-Lessons_Learned.md": "# 📚 LESSONS LEARNED\n*(Sẽ cập nhật sau khi dự án hoàn thành)*"
}

def scaffold_project():
    print("🚀 Bắt đầu khởi tạo Inventory Refactoring Project Alpha...")
    
    # Tạo thư mục dự án nếu chưa có
    os.makedirs(PROJECT_DIR, exist_ok=True)
    print(f"📁 Đã tạo/kiểm tra thư mục: {PROJECT_DIR}")

    # Tạo các file Markdown
    for filename, content in FILES_TO_CREATE.items():
        filepath = os.path.join(PROJECT_DIR, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ Đã tạo file: {filename}")
        else:
            print(f"  ⚠️ File đã tồn tại (Bỏ qua để tránh ghi đè): {filename}")

    print("\n🎉 Scaffold hoàn tất! Ní mở Obsidian lên để bắt đầu Phase 1 nhé.")

if __name__ == "__main__":
    scaffold_project()