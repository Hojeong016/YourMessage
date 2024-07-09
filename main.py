
import os
from openai import OpenAI
import streamlit as st
import pandas as pd
from base64 import b64encode



os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

image_path_map = {
    "매우 위험": "scoreImg/5.jpg",
    "위험": "scoreImg/4.jpg",
    "확인 필요": "scoreImg/3.jpg",
    "안전": "scoreImg/2.jpg",
    "매우 안전": "scoreImg/1.jpg"
}

st.markdown("""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta name="naver-site-verification" content="naver1c9a3278fb62fa5ab61d951fb51c72f1.html" />
</head>
<body>
</body>
</html>
""", unsafe_allow_html=True)

# CSS 스타일 지정
st.markdown("""
<style>
/* 라이트 모드 스타일 */
.section-title {
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 10px;
}
.section-description {
    font-size: 15px;
    color: #666666;
    margin-bottom: 20px;
}

.section-line {
    border-top: 1px solid #dddddd;
    margin-bottom: 20px;
}

.responsive-table {
    width: 100%;
    max-width: 100%;
    border-collapse: collapse;
    overflow-x: auto;
    display: block;
}

.responsive-table th, .responsive-table td {
    padding: 8px;
    text-align: left;
    border: 1px solid #dddddd;
}

/* 첫 번째 행의 열들에 대한 스타일 */
.responsive-table th:first-child {
    min-width: 140px; /* 첫 번째 열의 최소 너비 설정 */
    max-width: 400px; /* 첫 번째 열의 최대 너비 설정 */
    white-space: nowrap; /* 줄바꿈 방지 */
}

/* 나머지 행들의 열들에 대한 스타일 */
.responsive-table th:not(:first-child),
.responsive-table td:not(:first-child) {
    min-width: 350px; /* 기본적인 최소 너비 설정 */
    max-width: 500px; /* 기본적인 최대 너비 설정 */
    white-space: normal; /* 나머지 행들은 줄바꿈되도록 설정 */
}

.footer {
    display: flex;
    justify-content: flex-end; 
    align-items: center; 
    padding: 10px; 
    border-top: 1px solid #dddddd; 
}

.footer-logo {
    width: 150px; 
    height: auto; 
    cursor: pointer; 
    margin-right: 10px; /* 이미지와 만든이 텍스트 간 간격을 조정 */
}

.footer-small-text {
    font-size: 10px; 
    margin-right: 10px; 
}

.footer-light-text {
    font-size: 10px; 
    color: #666666; 
}

.reference-info {
    font-size: 10px; 
    color: #666666; 
    margin-top: 5px; 
}

/* 다크 모드 스타일 */
@media (prefers-color-scheme: dark) {
    .section-title {
        color: #ffffff;
    }
    .section-description {
        color: #ffffff;
    }
    .section-line {
        border-top: 1px solid #444444;
    }
    .responsive-table th {
        background-color: #6b9ea1;
        color: #ffffff;
    }
    .responsive-table td {
        border: 1px solid #444444;
        color: #dddddd;
    }
    .footer {
        border-top: 1px solid #444444;
    }
    .footer-small-text, .footer-light-text {
        color: #bbbbbb;
    }
    .reference-info {
        color: #bbbbbb;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='section-title'>너의 문자는&#128233;</div>", unsafe_allow_html=True)

st.markdown("<div class='section-line'></div>", unsafe_allow_html=True)

# 섹션 설명 출력
st.markdown("""
<div class='section-description'>
    비영리 공익광고 모임 '발광'에서 스미싱 문자 사기를 예방하기 위해 만든 '너의문자는'을 소개합니다.<br> 
    금융감독원에 따르면, 스미싱 피해액의 93.9%가 50대 이상 연령층에서 발생하고 있다고 합니다.<br>  
    이 서비스를 통해 부모님들이 안전하게 문자 서비스를 이용하실 수 있도록 도와드리고자 하니, <br> 
    많이 사용해 주시기 바랍니다.
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='section-line'></div>", unsafe_allow_html=True)

keyword = st.text_area("의심되는 문자를 입력 후 확인을 눌러주세요.")

if st.button('확인:mag_right:'): 
    with st.spinner('문자를 확인하고 있습니다'):
        # 첫 번째 요청: 스팸 여부 확인 및 점수 반환
            chat_completion1 = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": keyword,
                    },
                    {
                        "role": "system",
                        "content": (
                            "이 문자가 스팸 또는 사기 문자인지 확인하고, 0에서 100 사이의 숫자로 사기 위험도를 점수로 알려줘.점수가 낮을수록(0에 가까울수록) 사기 위험이 크고,높을수록(100에 가까울수록) 안전해. 이때 분석 내용은 알려주지말고 점수만 알려줘 0~100까지 숫자로만 "
                    
                        ),
                    }
                ],
                model="gpt-4o",
            )

        # 첫 번째 요청의 응답에서 점수 추출
            score = int(chat_completion1.choices[0].message.content.strip())
        
        # 점수를 기준으로 response 결정
            if 0 <= score <= 20:
                response = "매우 위험"
            elif 21 <= score <= 40:
                response = "위험"
            elif 41 <= score <= 60:
                response = "확인 필요"
            elif 61 <= score <= 80:
                response = "안전"
            else:
                response = "매우 안전"

            # 결과 출력
            # st.write(f"점수 판단 결과: {response}")
            
              # response에 따른 이미지 추가
            if response in image_path_map:
                image_path = image_path_map[response]
                st.image(image_path, caption=response, width=150)
        
        
        # 두 번째 요청: 점수 판단 근거 설명 요청
            chat_completion2 = client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": keyword,
                    },
                    {
                        "role": "system",
                        "content": (
                            "문자를 객관적으로 분석하여 아래의 일곱가지 기준으로 설명해줘"
                            "발신자 정보 : (예시 <국제 발신>인데 국내 기업의 내용을 담고 있는 경우, <웹 발신>인 경우에는 어떤 국가에서 발신하고 있는지 요약해줘 또한 발신자 정보에 대해 더 자세히 언급해줘)"
                            "의심스러운 링크 : (예시 링크의 철자에 오류 유무와 클릭 유도가 없는지 분석해줘)" 
                            "긴급성 강조 :"
                            "금전적 요구 :"
                            "철자 오류 :"
                            "의심 키워드 : (스팸의심 키워드가 있는지 파악해줘)"
                            "이 외의 사유 :"
                            "각 기준에 대해 세 줄 이내로 친절하고 쉽게 설명해줘 존댓말을 사용했으면 좋겠어. 목록화된 결과로 번호없이 글자와 : 만 출력해줘."
                        ),
                    }
                ],
                model="gpt-4o",
            )
        
        # 두 번째 요청의 응답
            result2 = chat_completion2.choices[0].message.content
            
        # 응답을 딕셔너리로 변환 (예시로 콜론을 기준으로 분리)
            ai_explanation = dict(item.split(": ") for item in result2.split("\n") if ": " in item)

        # 딕셔너리를 데이터프레임으로 변환
            df = pd.DataFrame(list(ai_explanation.items()), columns=["기준", "설명"])
            
        # 테이블을 HTML로 변환
            table_html = df.to_html(index=False, escape=False)

        # 테이블 이름 지정
            st.write("<strong><판단 근거 설명></strong>",  unsafe_allow_html=True)

        # 테이블 표시
            st.markdown(f'<div class="responsive-table">{table_html}</div>', unsafe_allow_html=True)
            
            st.markdown("<div class='reference-info'><strong> &#128680; AI를 활용하여 최대한 많은 테스트를 진행하였습니다. <br> 다만 100% 정확하진 않을수 있으니 의심이 가는 문자는 주의하세요.</strong></div>", unsafe_allow_html=True)
            st.markdown("<br><br>", unsafe_allow_html=True)     

# 참조 정보 출력
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("<div class='footer'>", unsafe_allow_html=True)

# logo 이미지를 클릭했을 때 이동할 링크 URL
link_url = "https://www.instagram.com/valgwang/"

# logo 이미지 파일 읽은 후 base64로 인코딩
with open('logoImg/logo.png', 'rb') as f:
    image_data = f.read()

image_base64 = b64encode(image_data).decode()

# logo 이미지에 링크 URL을 적용하여 HTML 코드 생성
image_html = f"<a href='{link_url}' target='_blank'><img src='data:image/png;base64,{image_base64}' class='footer-logo' style='cursor: pointer; width: 150px;'></a>"

with open('logoImg/instarLogo.png', 'rb') as f:
    instar_image_data = f.read()
    
instar_image_base64 = b64encode(instar_image_data).decode()

instar_image_html = f"<img src='data:image/jpeg;base64,{instar_image_base64}' alt='instarLogo' width='12'/>"

st.markdown(image_html, unsafe_allow_html=True)
st.markdown("<div  class='footer-small-text'>발광 | 세상을 밝히는 광고</div>", unsafe_allow_html=True)
st.markdown("<div  class='footer-light-text'>&#128231;Levi.yonghun@gmail.com</div>", unsafe_allow_html=True)
st.markdown(f"<div  class='footer-light-text'>{instar_image_html} @valgwang</div>", unsafe_allow_html=True)
st.markdown("<div></div>", unsafe_allow_html=True)
st.markdown("<div  class='footer-small-text'>도움 주신 분: 채호정</div>", unsafe_allow_html=True)
st.markdown("<div  class='footer-light-text'>&#128231;coghwjd4051@gmail.com</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
