# lambda/index.py
import json
import os
import urllib.request

# 環境変数から推論 API の URL を取得
PREDICT_API_URL = os.environ.get("https://d51c-34-148-77-72.ngrok-free.app/predict")

def lambda_handler(event, context):
    try:
        # 1) リクエストボディの読み取り
        body = json.loads(event["body"])
        message = body.get("message", "")
        history = body.get("conversationHistory", [])

        # 2) 推論用 API へ POST リクエスト
        payload = json.dumps({"message": message}).encode("utf-8")
        req = urllib.request.Request(
            PREDICT_API_URL,
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read())

        # 3) レスポンス解析 & 会話履歴の更新
        assistant = result.get("response", "")
        new_history = history + [
            {"role": "user", "content": message},
            {"role": "assistant", "content": assistant}
        ]

        # 4) 成功レスポンスの返却
        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": True,
                "response": assistant,
                "conversationHistory": new_history
            })
        }

    except Exception as e:
        # エラーハンドリング
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({
                "success": False,
                "error": str(e)
            })
        }
