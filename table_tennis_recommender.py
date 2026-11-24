import random
import streamlit as st


st.set_page_config(
    page_title="맞춤형 탁구채 추천!",
    page_icon="🏓",
    layout="centered",
)

# 실제 판매 페이지·가격비교 페이지에서 확인한 제품 목록입니다.
# 가격은 조사 당시 표시된 참고 가격이며, 판매처·시점에 따라 달라질 수 있습니다.
# weight_min / weight_max는 완성 라켓 전체 무게(g)입니다.
# 전체 무게가 공개되지 않은 핌플 조합은 None으로 두었습니다.
PRODUCTS = [
    {
        "name": "엑시옴 M 6.0 P",
        "styles": ["공격적"],
        "price": 65000,
        "weight_min": 150,
        "weight_max": 150,
        "weight_text": "약 150g",
        "description": "펜홀더 완제품 라켓입니다. 드라이브와 공격적인 플레이를 선호하는 사용자에게 고려할 만한 제품입니다.",
        "type": "펜홀더 완제품",
        "price_note": "엑시옴 공식 스토어 표시 판매가",
        "url": "https://xiom.store/product/m-60-p-%EC%99%84%EC%A0%9C%ED%92%88-%EB%9D%BC%EC%BC%93/78/",
        "source": "엑시옴 공식 스토어 판매가, 다나와 무게 정보",
    },
    {
        "name": "엑시옴 참피온 V 3.0 S",
        "styles": ["수비적"],
        "price": 29900,
        "weight_min": 170,
        "weight_max": 170,
        "weight_text": "약 170g",
        "description": "5겹 합판의 올라운드 완제품입니다. 전문 수비 전용 라켓은 아니지만, 안정적인 컨트롤을 중요하게 생각하는 플레이어의 참고 제품으로 분류했습니다.",
        "type": "쉐이크핸드 완제품",
        "price_note": "판매 페이지 표시 판매가",
        "url": "https://shinsegaemall.ssg.com/item/itemView.ssg?itemId=1000677759635&salestrNo=6005&siteNo=6004",
        "source": "신세계몰 표시 판매가, 다나와 무게 정보",
    },
    {
        "name": "버터플라이 와카바 3000",
        "styles": ["수비적"],
        "price": 30890,
        "weight_min": 168,
        "weight_max": 168,
        "weight_text": "약 168g",
        "description": "5겹 합판의 러버 부착 완제품입니다. 초보자가 기본기를 익히거나 안정적인 컨트롤을 연습할 때 참고할 만한 제품입니다.",
        "type": "쉐이크핸드 완제품",
        "price_note": "다나와 가격비교 최저가 표시 기준",
        "url": "https://prod.danawa.com/info/?pcode=2466653",
        "source": "다나와 가격비교 및 SSG 상품 정보",
    },
    {
        "name": "버터플라이 코르벨 + 로제나 러버 조합",
        "styles": ["공격적"],
        "price": 124000,
        "weight_min": 185,
        "weight_max": 195,
        "weight_text": "약 185~195g",
        "description": "코르벨 목판에 양면 로제나 러버를 부착한 조합입니다. 드라이브 중심의 공격적인 플레이를 고려하는 사용자에게 어울리는 조합입니다.",
        "type": "목판 + 양면 러버 조합",
        "price_note": "더스포츠샵 표시 판매가",
        "url": "https://m.thesportsshop.co.kr/product/detail.html?cate_no=723&display_group=1&product_no=4863",
        "source": "더스포츠샵 상품 정보",
    },
    {
        "name": "버터플라이 코르벨 + 오메가2 + 로제나 조합",
        "styles": ["공격적"],
        "price": 142000,
        "weight_min": 185,
        "weight_max": 195,
        "weight_text": "약 185~195g",
        "description": "코르벨 목판과 양면 러버로 구성된 조합입니다. 비교적 무게감 있는 공격형 라켓을 원하는 사용자에게 참고가 됩니다.",
        "type": "목판 + 양면 러버 조합",
        "price_note": "판매 페이지 표시 가격",
        "url": "https://www.coupang.com/vp/products/7383568525?itemId=19074149221&vendorItemId=86196689007",
        "source": "쿠팡 상품 정보",
    },
    {
        "name": "버터플라이 다이오드 V + 줄라 다이나리즈 AGR / 빅타스 컬 P1V",
        "styles": ["핌플"],
        "price": 155000,
        "weight_min": None,
        "weight_max": None,
        "weight_text": "완성 라켓 전체 무게 미표기",
        "description": "수비형 다이오드 V 목판과 롱핌플 컬 P1V 등을 조합한 라켓 세트입니다. 롱핌플을 사용하는 플레이에 관심 있는 사람을 위한 제품입니다.",
        "type": "롱핌플 조합 세트",
        "price_note": "더블스포츠 표시 판매가",
        "url": "https://doublesports.kr/product/%EB%A1%B1%ED%95%8C%ED%94%8C%EC%84%B8%ED%8A%B8-%EB%B2%84%ED%84%B0%ED%94%8C%EB%9D%BC%EC%9D%B4-%EB%8B%A4%EC%9D%B4%EC%98%A4%EB%93%9C-v-%EC%A4%84%EB%9D%BC-%EB%8B%A4%EC%9D%B4%EB%82%98%EB%A6%AC%EC%A6%88-agr-%EB%B9%85%ED%83%80%EC%8A%A4-%EC%BB%ACp1v/1554",
        "source": "더블스포츠 상품 정보",
    },
    {
        "name": "닛타쿠 어쿠스틱 카본 + 파스탁 G-1 / 모리스토 SP 조합",
        "styles": ["핌플"],
        "price": 255000,
        "weight_min": None,
        "weight_max": None,
        "weight_text": "완성 라켓 전체 무게 미표기",
        "description": "닛타쿠 어쿠스틱 카본 목판에 숏핌플 모리스토 SP 등을 조합한 세트입니다. 숏핌플을 활용한 빠른 공격 스타일을 고려하는 사람을 위한 제품입니다.",
        "type": "숏핌플 조합 세트",
        "price_note": "더블스포츠 표시 판매가",
        "url": "https://doublesports.kr/product/detail.html?cate_no=42&display_group=1&product_no=1556",
        "source": "더블스포츠 상품 정보",
    },
]

# 프로그램에 넣은 탁구채 예시 사진입니다. 선택한 제품 자체의 사진은 아닙니다.
RACKET_IMAGE_URL = (
    "https://joola.fr/cdn/shop/files/"
    "54207_JOOLA_InfinityCarbon_04_web_b8ed6cb3-c55b-4f6f-9c9c-c49122362a32.jpg"
    "?v=1753177664&width=1200"
)


def find_matching_rackets(style, budget, weight):
    """선택한 플레이 스타일·예산·무게에 맞는 제품을 리스트에서 찾습니다."""
    matches = []
    weight_unknown = []

    # 반복문으로 제품 목록을 하나씩 확인합니다.
    for racket in PRODUCTS:
        # 조건문으로 플레이 스타일을 확인합니다.
        if style not in racket["styles"]:
            continue

        # 조건문으로 예산을 확인합니다.
        if budget == "저가 (10만 원 이하)":
            if racket["price"] > 100000:
                continue
        elif budget == "고가 (10만 원 이상)":
            if racket["price"] < 100000:
                continue

        # 전체 무게가 공개되지 않은 제품은 정확한 무게 필터에서 따로 분리합니다.
        if racket["weight_min"] is None or racket["weight_max"] is None:
            weight_unknown.append(racket)
            continue

        # 무게 기준은 180g입니다.
        if weight == "가벼움 (180g 이하)":
            if racket["weight_max"] <= 180:
                matches.append(racket)
        elif weight == "무거움 (180g 초과)":
            if racket["weight_min"] > 180:
                matches.append(racket)

    return matches, weight_unknown


def show_selected_conditions(style, budget, weight):
    """선택한 조건을 목록으로 화면에 출력합니다."""
    conditions = [
        ("플레이 스타일", style),
        ("예산", budget),
        ("무게", weight),
    ]

    # 반복문으로 조건 목록을 하나씩 출력합니다.
    for condition_name, condition_value in conditions:
        st.markdown(f"- **{condition_name}:** {condition_value}")


def show_recommendation(racket, style, budget, weight):
    """추천 문구, 조건, 사진, 가격과 제품 설명을 순서대로 표시합니다."""
    st.success(f"당신의 맞춤형 탁구채는 **{racket['name']}**입니다")

    st.subheader("선택한 조건")
    show_selected_conditions(style, budget, weight)

    # 사진을 가격보다 위에 배치합니다.
    st.image(
        RACKET_IMAGE_URL,
        caption="탁구채 예시 사진입니다. 실제 추천 제품의 사진과 다를 수 있습니다.",
        use_container_width=True,
    )

    st.subheader("가격")
    st.markdown(f"### {racket['price']:,}원")
    st.caption(racket["price_note"] + " · 실제 가격은 판매처에서 다시 확인하세요.")

    st.write(f"**무게:** {racket['weight_text']}")
    st.write(f"**제품 형태:** {racket['type']}")
    st.write(racket["description"])
    st.link_button("제품 정보 확인하기", racket["url"], use_container_width=True)


st.title("🏓 맞춤형 탁구채 추천!")
st.write("아래 조건을 버튼으로 선택한 뒤 **찾아보기**를 눌러 보세요.")

st.subheader("1. 플레이 스타일")
play_style = st.segmented_control(
    "플레이 스타일",
    options=["공격적", "수비적", "핌플"],
    default="공격적",
    label_visibility="collapsed",
    key="play_style",
)

st.subheader("2. 예산")
budget = st.segmented_control(
    "예산",
    options=["저가 (10만 원 이하)", "고가 (10만 원 이상)"],
    default="저가 (10만 원 이하)",
    label_visibility="collapsed",
    key="budget",
)

st.subheader("3. 무게")
weight = st.segmented_control(
    "무게",
    options=["가벼움 (180g 이하)", "무거움 (180g 초과)"],
    default="가벼움 (180g 이하)",
    label_visibility="collapsed",
    key="weight",
)

st.caption(
    "분류 기준: 저가는 10만 원 이하, 고가는 10만 원 이상입니다. "
    "가벼움은 180g 이하, 무거움은 180g 초과입니다. "
    "무게는 완성 라켓 전체 무게 기준이며, 10만 원은 두 예산 선택에 모두 포함됩니다."
)

if st.button("찾아보기", type="primary", use_container_width=True):
    if play_style is None or budget is None or weight is None:
        st.warning("플레이 스타일, 예산, 무게를 모두 선택해 주세요.")
    else:
        matching_rackets, unknown_weight_rackets = find_matching_rackets(
            play_style, budget, weight
        )

        st.divider()
        st.subheader("추천 결과")

        # 조건에 맞는 제품이 있으면 그중 하나를 무작위로 추천합니다.
        if matching_rackets:
            selected_racket = random.choice(matching_rackets)
            show_recommendation(selected_racket, play_style, budget, weight)
        else:
            st.warning("선택한 세 가지 조건을 모두 만족하는 제품을 찾지 못했습니다.")

            if unknown_weight_rackets:
                st.info(
                    "아래 제품은 플레이 스타일과 예산에는 맞지만, 판매 페이지에서 "
                    "완성 라켓 전체 무게를 확인할 수 없어 가벼움/무거움 조건을 판정할 수 없습니다."
                )
                for racket in unknown_weight_rackets:
                    st.markdown(f"- **{racket['name']}** — {racket['price']:,}원, 무게 미표기")
                    st.caption(racket["description"])
                    st.link_button(
                        f"{racket['name']} 제품 정보 확인",
                        racket["url"],
                        use_container_width=True,
                    )

st.divider()
st.caption(
    "제품 데이터는 실제 판매·가격비교 페이지에서 확인한 모델을 바탕으로 했습니다. "
    "가격과 재고는 바뀔 수 있으며, 플레이 스타일별 분류는 추천 프로그램을 위한 참고 분류입니다. "
    "예시 사진은 추천된 제품의 실제 사진이 아닐 수 있습니다."
)
