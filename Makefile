# デフォルト環境
ENV ?= dev

# Poetryコマンド
POETRY = poetry run

# アプリケーション起動
run:
	@echo "Starting FastAPI application with ENV=$(ENV)"
	@if [ ! -f .env.$(ENV) ]; then \
		echo "Error: .env.$(ENV) file not found"; \
		exit 1; \
	fi
	ENV=$(ENV) $(POETRY) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 --log-level debug

# テスト実行
test:
	@echo "Running tests..."
	$(POETRY) pytest

# テスト実行（カバレッジ付き）
test-cov:
	@echo "Running tests with coverage..."
	ENV=test $(POETRY) pytest --cov=app --cov-report=html

# コードフォーマット
format:
	@echo "Formatting code..."
	$(POETRY) black .
	$(POETRY) isort .

# リント実行
lint:
	@echo "Running linter..."
	$(POETRY) flake8 app/ tests/

# 依存関係インストール
install:
	@echo "Installing dependencies..."
	poetry install

# 依存関係更新
update:
	@echo "Updating dependencies..."
	poetry update

# 開発サーバー起動（開発環境）
dev:
	@echo "Starting development server..."
	ENV=dev $(POETRY) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 本番サーバー起動（本番環境）
prod:
	@echo "Starting production server..."
	ENV=prod $(POETRY) uvicorn app.main:app --host 0.0.0.0 --port 8000

# Serverless Frameworkでデプロイ
deploy-serverless:
	@echo "Deploying with Serverless Framework..."
	VERSION=$$(./scripts/get_version.sh) serverless deploy --stage dev

# Serverless Frameworkで削除
remove-serverless:
	@echo "Removing Serverless deployment..."
	serverless remove --stage dev

deploy-serverless-prod:
	@echo "Deploying with Serverless Framework..."
	VERSION=$$(./scripts/get_version.sh) serverless deploy --stage v1

remove-serverless-prod:
	@echo "Removing Serverless deployment..."
	serverless remove --stage v1

# ヘルプ表示
help:
	@echo "Available commands:"
	@echo "  make run ENV=dev         - Start with development environment"
	@echo "  make run ENV=prod        - Start with production environment"
	@echo "  make test                - Run tests"
	@echo "  make test-cov            - Run tests with coverage"
	@echo "  make format              - Format code"
	@echo "  make lint                - Run linter"
	@echo "  make install             - Install dependencies"
	@echo "  make update              - Update dependencies"
	@echo "  make dev                 - Start development server"
	@echo "  make prod                - Start production server"
	@echo "  make deploy-serverless   - Deploy with Serverless Framework"
	@echo "  make remove-serverless   - Remove Serverless deployment"
	@echo "  make help                - Show this help"

.PHONY: run test test-cov format lint install update dev prod deploy-serverless remove-serverless help 