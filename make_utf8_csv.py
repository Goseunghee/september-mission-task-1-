import pandas as pd

input_file = "한국무역보험공사_국가별 신용장방식 결제비중_20211231.xlsx"
output_file = "한국무역보험공사_국가별 신용장방식 결제비중_20211231_utf8.csv"

df = pd.read_excel(input_file)
df.to_csv(output_file, index=False, encoding="utf-8-sig")

print("UTF-8 CSV 생성 완료!")