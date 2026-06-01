import csv
import random
import uuid
from datetime import datetime, timedelta

# --- 1. 定义数据生成的参数 ---

# 输出的CSV文件名
OUTPUT_FILENAME = "bank_transactions.csv"

# 生成的记录总数
NUM_RECORDS = 300

# 定义可能的数据值
INSTITUTIONS = [f"INST{str(i).zfill(3)}" for i in range(1, 11)]  # 10个机构
TRANSACTION_TYPES = ["转账", "收款", "取现", "存款", "代付", "代收"]

# --- 2. 生成基础数据列表 ---

# 为了模拟真实的客户和账户关系，我们先创建一批客户和账户
customers = []
for i in range(1, 201):  # 创建200个客户
    customer_id = f"CUST{str(i).zfill(4)}"
    # 每个客户随机拥有1-3个账户
    num_accounts = random.randint(1, 3)
    for j in range(num_accounts):
        institution_code = random.choice(INSTITUTIONS)
        # 生成一个看起来像真实卡号的账号
        account_number = f"622{random.randint(100, 999)}{random.randint(1000000000, 9999999999)}"
        customers.append({
            "customer_id": customer_id,
            "account_number": account_number,
            "institution_code": institution_code
        })

# --- 3. 生成交易记录 ---

transactions = []
# 定义日期范围：最近30天
end_date = datetime.now()
start_date = end_date - timedelta(days=30)

for _ in range(NUM_RECORDS):
    # 随机选择一个主账户作为交易方
    main_account = random.choice(customers)

    # 随机生成一个日期
    random_days = random.randint(0, 30)
    transaction_date = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%d")

    # 生成唯一的交易流水号
    transaction_id = f"TRX-{uuid.uuid4().hex[:8].upper()}"

    # 随机选择交易类型
    trx_type = random.choice(TRANSACTION_TYPES)

    # 根据交易类型生成不同的交易记录
    if trx_type in ["转账", "代付"]:
        # 支出交易：金额为负
        amount = -round(random.uniform(10, 50000), 2)
        # 随机选择一个对方账户（跨行或本行）
        counterparty_account = random.choice(customers)
        counterparty_institution = counterparty_account["institution_code"]
        counterparty_account_number = counterparty_account["account_number"]

    elif trx_type in ["收款", "代收"]:
        # 收入交易：金额为正
        amount = round(random.uniform(10, 50000), 2)
        # 随机选择一个对方账户
        counterparty_account = random.choice(customers)
        counterparty_institution = counterparty_account["institution_code"]
        counterparty_account_number = counterparty_account["account_number"]

    elif trx_type == "取现":
        # 支出交易：金额为负
        amount = -round(random.uniform(100, 2000), 2)
        # 取现没有对方机构和账号
        counterparty_institution = ""
        counterparty_account_number = ""

    elif trx_type == "存款":
        # 收入交易：金额为正
        amount = round(random.uniform(100, 50000), 2)
        # 存款没有对方机构和账号
        counterparty_institution = ""
        counterparty_account_number = ""

    # 构造交易记录
    transaction_record = {
        "日期": transaction_date,
        "机构编码": main_account["institution_code"],
        "账号": main_account["account_number"],
        "客户号": main_account["customer_id"],
        "交易流水号": transaction_id,
        "对方机构编码": counterparty_institution,
        "对方账号": counterparty_account_number,
        "交易方式": trx_type,
        "交易金额": amount
    }
    transactions.append(transaction_record)

# --- 4. 将数据写入CSV文件 ---

# 定义CSV文件的表头
fieldnames = ["日期", "机构编码", "账号", "客户号", "交易流水号", "对方机构编码", "对方账号", "交易方式", "交易金额"]

with open(OUTPUT_FILENAME, 'w', newline='', encoding='utf-8-sig') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # 写入表头
    writer.writeheader()

    # 写入所有交易记录
    writer.writerows(transactions)

print(f"CSV数据集已成功生成，共 {NUM_RECORDS} 条记录。")
print(f"文件保存在: {OUTPUT_FILENAME}")