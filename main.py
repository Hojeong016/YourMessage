import os
from openai import OpenAI
import streamlit as st
import pandas as pd

image_path_map = {
    "매우 위험": "scoreImg/5.jpg",
    "위험": "scoreImg/4.jpg",
    "확인 필요": "scoreImg/3.jpg",
    "안전": "scoreImg/2.jpg",
    "매우 안전": "scoreImg/1.jpg"
}

os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

st.title('너의 문자는')

keyword = st.text_area("문자를 입력해주세요")

if st.button('확인하기'): 
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
                st.image(image_path, caption=response,  width=150)
        
        
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
            df = pd.DataFrame(list(ai_explanation.items()), columns=["기준", "설명"], index=["1", "2", "3", "4", "5", "6", "7"])

            # 테이블 이름 지정
            st.write("<판단 근거 설명>",  unsafe_allow_html=True)

            # 테이블 표시
            st.table(df)