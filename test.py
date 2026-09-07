import os
import pandas as pd

# 1. 파일 경로 설정
filename = r"C:\Users\user\Desktop\신용장방식\한국무역보험공사_국가별 신용장방식 결제비중_20211231.xlsx"

# 2. 파일 존재 확인
print("파일 존재 여부:", os.path.exists(filename))

if not os.path.exists(filename):
    print("파일 경로를 다시 확인하세요.")
else:
    # 3. 엑셀 파일 읽기
    df = pd.read_excel(filename, sheet_name=0)

    # 4. 원본 데이터 확인
    print("\n[원본 데이터 상위 5행]")
    print(df.head())

    print("\n[컬럼명]")
    print(df.columns.tolist())

    print("\n[행, 열 개수]")
    print(df.shape)

    print("\n[결측치 개수]")
    print(df.isnull().sum())

    # 5. wide -> long format 변환
    df_long = df.melt(
        id_vars='국가명',
        value_vars=[2017, 2018, 2019, 2020, 2021],
        var_name='연도',
        value_name='신용장비중'
    )

    # 6. 데이터 타입 정리
    df_long['연도'] = df_long['연도'].astype(int)

    print("\n[long format 상위 10행]")
    print(df_long.head(10))

    print("\n[long format 크기]")
    print(df_long.shape)

    # 7. 연도별 평균 계산
    yearly_mean = df_long.groupby('연도', as_index=False)['신용장비중'].mean()

    print("\n[연도별 전체 평균 신용장 비중]")
    print(yearly_mean)

    # 8. 국가별 평균, 표준편차 계산
    country_stats = df_long.groupby('국가명')['신용장비중'].agg(['mean', 'std']).reset_index()
    country_stats.columns = ['국가명', '평균비중', '표준편차']

    print("\n[국가별 평균/표준편차 상위 10행]")
    print(country_stats.head(10))

    # 9. 평균 비중이 높은 국가 TOP 10
    top10_mean = country_stats.sort_values('평균비중', ascending=False).head(10)

    print("\n[평균 신용장 비중이 높은 국가 TOP 10]")
    print(top10_mean)

    # 10. 평균 비중이 낮은 국가 TOP 10
    bottom10_mean = country_stats.sort_values('평균비중', ascending=True).head(10)

    print("\n[평균 신용장 비중이 낮은 국가 TOP 10]")
    print(bottom10_mean)

    # 11. 변동성이 큰 국가 TOP 10
    top10_std = country_stats.sort_values('표준편차', ascending=False).head(10)

    print("\n[변동성(표준편차)이 큰 국가 TOP 10]")
    print(top10_std)

    # 12. 2021년 기준 정렬
    top2021 = df[['국가명', 2021]].sort_values(by=2021, ascending=False).head(10)

    print("\n[2021년 신용장 비중 TOP 10]")
    print(top2021)

    # 13. 2017 -> 2021 변화폭 계산
    df['변화폭'] = df[2021] - df[2017]
    change_top = df[['국가명', '변화폭']].sort_values(by='변화폭', ascending=False).head(10)
    change_bottom = df[['국가명', '변화폭']].sort_values(by='변화폭', ascending=True).head(10)

    print("\n[2017→2021 증가폭 TOP 10]")
    print(change_top)

    print("\n[2017→2021 감소폭 TOP 10]")
    print(change_bottom)

    # 14. 결과 저장
    save_folder = r"C:\Users\user\Desktop\신용장방식"

    df_long.to_excel(os.path.join(save_folder, "신용장_long_format.xlsx"), index=False)
    yearly_mean.to_excel(os.path.join(save_folder, "연도별_평균_신용장비중.xlsx"), index=False)
    country_stats.to_excel(os.path.join(save_folder, "국가별_평균_표준편차.xlsx"), index=False)
    top10_mean.to_excel(os.path.join(save_folder, "평균비중_TOP10.xlsx"), index=False)
    bottom10_mean.to_excel(os.path.join(save_folder, "평균비중_BOTTOM10.xlsx"), index=False)
    top10_std.to_excel(os.path.join(save_folder, "변동성_TOP10.xlsx"), index=False)
    top2021.to_excel(os.path.join(save_folder, "2021년_TOP10.xlsx"), index=False)
    change_top.to_excel(os.path.join(save_folder, "증가폭_TOP10.xlsx"), index=False)
    change_bottom.to_excel(os.path.join(save_folder, "감소폭_TOP10.xlsx"), index=False)

    print("\n결과 파일 저장 완료!")