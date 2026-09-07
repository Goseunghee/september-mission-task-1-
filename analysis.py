import os
import pandas as pd
import matplotlib.pyplot as plt

# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

# 폴더 생성
os.makedirs("images", exist_ok=True)
os.makedirs("results", exist_ok=True)

# 엑셀 파일 경로
file_path = "한국무역보험공사_국가별 신용장방식 결제비중_20211231.xlsx"

# 엑셀 읽기
df = pd.read_excel(file_path)

print("[원본 데이터 상위 5행]")
print(df.head())
print("\n[컬럼명]")
print(df.columns.tolist())

# 컬럼명 정리
df.columns = df.columns.map(str)
df.columns = [col.strip() for col in df.columns]

# 첫 번째 컬럼명을 국가명으로 통일
df = df.rename(columns={df.columns[0]: '국가명'})

year_cols = ['2017', '2018', '2019', '2020', '2021']

# 퍼센트 문자열 -> 숫자형 변환
for col in year_cols:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace('%', '', regex=False)
        .str.strip()
        .astype(float) / 100
    )

print("\n[변환 후 데이터 상위 5행]")
print(df.head())

# 결측치 확인
print("\n[결측치 개수]")
print(df.isnull().sum())

# wide -> long 변환
df_long = df.melt(
    id_vars='국가명',
    value_vars=year_cols,
    var_name='연도',
    value_name='신용장비중'
)

df_long['연도'] = df_long['연도'].astype(int)

print("\n[long format 상위 5행]")
print(df_long.head())
print("\n[long format 크기]")
print(df_long.shape)

# 1. 연도별 평균
yearly_mean = df_long.groupby('연도', as_index=False)['신용장비중'].mean()
print("\n[연도별 평균]")
print(yearly_mean)
yearly_mean.to_csv("results/yearly_mean.csv", index=False, encoding='utf-8-sig')

# 2. 국가별 평균/표준편차
country_stats = df_long.groupby('국가명')['신용장비중'].agg(['mean', 'std']).reset_index()
country_stats.columns = ['국가명', '평균비중', '표준편차']
country_stats = country_stats.sort_values(by='평균비중', ascending=False)

print("\n[국가별 평균/표준편차 상위 10개]")
print(country_stats.head(10))
country_stats.to_csv("results/country_stats.csv", index=False, encoding='utf-8-sig')

# 3. 2021년 상위 10개 국가
top2021 = df[['국가명', '2021']].sort_values(by='2021', ascending=False).head(10)

print("\n[2021년 상위 10개 국가]")
print(top2021)
top2021.to_csv("results/top2021.csv", index=False, encoding='utf-8-sig')

# 4. 2017 -> 2021 변화폭
df['변화폭'] = df['2021'] - df['2017']

increase_top10 = df[['국가명', '변화폭']].sort_values(by='변화폭', ascending=False).head(10)
decrease_top10 = df[['국가명', '변화폭']].sort_values(by='변화폭', ascending=True).head(10)

print("\n[증가폭 상위 10개]")
print(increase_top10)

print("\n[감소폭 상위 10개]")
print(decrease_top10)

increase_top10.to_csv("results/increase_top10.csv", index=False, encoding='utf-8-sig')
decrease_top10.to_csv("results/decrease_top10.csv", index=False, encoding='utf-8-sig')

change_top = pd.concat([increase_top10, decrease_top10], axis=0)

# 그래프 1: 연도별 평균 추세
plt.figure(figsize=(8, 5))
plt.plot(yearly_mean['연도'], yearly_mean['신용장비중'], marker='o', color='royalblue', linewidth=2)

for x, y in zip(yearly_mean['연도'], yearly_mean['신용장비중']):
    plt.text(x, y + 0.003, f"{y:.3f}", ha='center')

plt.title('연도별 평균 신용장 결제비중 추이 (2017~2021)')
plt.xlabel('연도')
plt.ylabel('평균 신용장 결제비중')
plt.grid(axis='y', linestyle='--', alpha=0.4)
plt.tight_layout()
plt.savefig("images/figure1_yearly_trend.png", dpi=300)
plt.close()

# 그래프 2: 2021년 상위 10개 국가
plt.figure(figsize=(9, 6))
plt.barh(top2021['국가명'], top2021['2021'], color='steelblue')
plt.gca().invert_yaxis()

for i, v in enumerate(top2021['2021']):
    plt.text(v + 0.01, i, f"{v:.2f}", va='center')

plt.title('2021년 국가별 신용장 결제비중 TOP 10')
plt.xlabel('신용장 결제비중')
plt.ylabel('국가명')
plt.tight_layout()
plt.savefig("images/figure2_top10_2021.png", dpi=300)
plt.close()

# 그래프 3: 2017~2021 변화폭
plt.figure(figsize=(10, 7))
colors = ['blue' if x > 0 else 'red' for x in change_top['변화폭']]
plt.barh(change_top['국가명'], change_top['변화폭'], color=colors)
plt.axvline(0, color='black', linewidth=1)

for i, v in enumerate(change_top['변화폭']):
    if v >= 0:
        plt.text(v + 0.01, i, f"{v:.2f}", va='center')
    else:
        plt.text(v - 0.08, i, f"{v:.2f}", va='center')

plt.title('2017년 대비 2021년 신용장 결제비중 변화폭')
plt.xlabel('변화폭 (2021 - 2017)')
plt.ylabel('국가명')
plt.tight_layout()
plt.savefig("images/figure3_change_2017_2021.png", dpi=300)
plt.close()

print("\n완료!")
print("- images 폴더 확인")
print("- results 폴더 확인")