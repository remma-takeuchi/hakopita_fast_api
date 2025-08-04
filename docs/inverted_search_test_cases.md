# 反転検索（enable_inverted_search）テストケース概要

## 概要

`enable_inverted_search`機能のテストケースを作成しました。この機能は、幅と奥行きのパラメータを入れ替えて検索を行い、より多くの検索結果を取得することを目的としています。

## テストデータ

反転検索専用の5件のテストデータを使用：

| ID | 幅(width) | 奥行き(depth) | 高さ(height) | カテゴリ | 用途 |
|---|---|---|---|---|---|
| width_20_depth_30_height_25 | 20cm | 30cm | 25cm | Box(0) | 基本テスト用 |
| width_30_depth_20_height_25 | 30cm | 20cm | 25cm | Box(0) | 反転検索確認用 |
| width_25_depth_35_height_25 | 25cm | 35cm | 25cm | Box(0) | 範囲検索用 |
| width_35_depth_25_height_25 | 35cm | 25cm | 25cm | Box(0) | 範囲検索用 |
| width_20_depth_30_height_30 | 20cm | 30cm | 30cm | Box(0) | 高さテスト用 |

## テストパターン

### 1. 幅20cm検索テスト (`test_inverted_search_width_20cm`)

**確認観点：** 
- 通常検索では幅20cmのアイテムのみが検索される
- 反転検索では幅20cm OR 奥行き20cmのアイテムが検索される

**期待値：**
- 通常検索：2件 (`width_20_depth_30_height_25`, `width_20_depth_30_height_30`)
- 反転検索：3件 (上記2件 + `width_30_depth_20_height_25`)

**結果：** ✅ 期待通りに動作

### 2. 奥行き20cm検索テスト (`test_inverted_search_depth_20cm`)

**確認観点：**
- 通常検索では奥行き20cmのアイテムのみが検索される
- 反転検索では奥行き20cm OR 幅20cmのアイテムが検索される

**期待値：**
- 通常検索：1件 (`width_30_depth_20_height_25`)
- 反転検索：3件 (`width_30_depth_20_height_25`, `width_20_depth_30_height_25`, `width_20_depth_30_height_30`)

**結果：** ✅ 期待通りに動作

### 3. 高さ30cm検索テスト (`test_inverted_search_height_30cm`)

**確認観点：**
- 高さパラメータは反転検索の対象外であることを確認
- 通常検索と反転検索で同じ結果が返される

**期待値：**
- 通常検索：1件 (`width_20_depth_30_height_30`)
- 反転検索：1件 (同じアイテム、変化なし)

**結果：** ✅ 期待通りに動作（高さは反転対象外）

### 4. 幅20-30cm範囲検索テスト (`test_inverted_search_width_range_20_30cm`)

**確認観点：**
- 範囲検索でも反転検索が正しく動作する
- 幅20-30cm OR 奥行き20-30cmの条件で検索される

**期待値：**
- 通常検索：4件 (`width_20_depth_30_height_25`, `width_30_depth_20_height_25`, `width_25_depth_35_height_25`, `width_20_depth_30_height_30`)
- 反転検索：5件 (上記4件 + `width_35_depth_25_height_25`)

**結果：** ✅ 期待通りに動作

## Fixture構成

### `setup_inverted_search_database`
- スコープ：function
- 機能：反転検索専用のテストデータベースを初期化
- 使用方法：各テスト関数の引数として指定

### `add_inverted_search_test_data`
- 機能：5件の専用テストデータをデータベースに挿入
- 特徴：既存のFixtureと競合しない独立したデータセット

## 検証結果

✅ **反転検索の動作確認**
- 幅（width）と奥行き（depth）パラメータが正しく入れ替わって検索される
- 高さ（height）パラメータは反転検索の対象外
- 単一値検索、範囲検索ともに正しく動作

✅ **既存機能への影響なし**
- 専用のFixtureとテストデータを使用
- 既存のテストケースに影響を与えない

✅ **テストカバレッジの向上**
- 反転検索機能の主要な動作パターンを網羅
- エッジケース（高さパラメータ、範囲検索）も含む

## 実行方法

```bash
# 反転検索テストのみ実行
python -m pytest tests/test_search_storage.py -k "inverted_search" -v

# 個別テスト実行例
python -m pytest tests/test_search_storage.py::test_inverted_search_width_20cm -v -s
```

## 技術的注意点

1. **storage_category統一**：すべてのテストデータでBox(0)に統一
2. **許容範囲**：サイズ検索では±0.5cmの許容範囲が適用される
3. **shop_id制限**：country_code=jpのデフォルト設定により、shop_id < 100のデータのみ検索対象
4. **ページネーション**：デフォルトでpage_size=2000のため、テストデータ5件は1ページ内に収まる 