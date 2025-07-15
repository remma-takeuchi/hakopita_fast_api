import os
import logging
from mangum import Mangum
from app.main import app

# ログ設定
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Mangumハンドラーを作成
handler = Mangum(app, lifespan="off")

def lambda_handler(event, context):
    """
    AWS Lambda用のハンドラー関数
    
    Args:
        event: API Gatewayからのイベント
        context: Lambdaコンテキスト
    
    Returns:
        API Gatewayレスポンス形式の辞書
    """
    logger.info(f"Lambda handler called with event: {event}")
    
    # デバッグ情報を追加
    if 'pathParameters' in event and event['pathParameters']:
        logger.info(f"Path parameters: {event['pathParameters']}")
    if 'path' in event:
        logger.info(f"Request path: {event['path']}")
    if 'rawPath' in event:
        logger.info(f"Raw path: {event['rawPath']}")
    
    try:
        # Mangumを使用してFastAPIアプリケーションを実行
        response = handler(event, context)
        logger.info(f"Lambda handler response: {response}")
        return response
    except Exception as e:
        logger.error(f"Lambda handler error: {e}")
        return {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "GET,POST,PUT,DELETE,OPTIONS"
            },
            "body": '{"error": "Internal server error"}'
        } 