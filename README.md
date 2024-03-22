# Chorus
音楽がユーザー交流の架け橋・まだ知らない音楽との架け橋となるSNS。

Spotify APIをベースとした、音楽にコメントをつけてユーザー同士が投稿できます。

## Detail
このシステムの技術仕様について

### Framework
 - Django

### Database
 - SQLite

### API
 - Spotify Web API

### Web Server
 - Nginx
 - Gunicorn

### Infrastructure
 - Azure Virtual Machine
   - OS: ubuntu 20.04
   - Size: Standard_B1s
   - Disk: 30GB
 - Amazon S3
 - Amazon Route 53
   - Host Zone
 - Google Domains

## Features
搭載した機能

### All
 - 全てのページでレスポンシブデザインを搭載
 - スマホ版は画面下部、PC版は画面左にメニューバーを表示

### Home
ユーザーが投稿した楽曲が表示されるビュー
 - スマホ版は3列で表示
 - アルバムアートをタッチして、楽曲ページへ

### Song
楽曲ごとに楽曲情報や投稿を閲覧するビュー
 - アーティスト名・アルバム名から各ページへ移動
 - Spotify埋め込みより、楽曲プレビュー
 - 他のアルバムに収録された同一楽曲を確認
 - ページ内から投稿ページへ移動

### Search
コンテンツを検索するビュー
 - コンテンツ種類ごとに分けて表示
 - Spotifyリンクを直接貼りつけ、適切なページへリダイレクト

### Spotify
ユーザーのプレイヤーを操作するビュー
 - Spotify OAuth 2.0認証より、過去に再生した楽曲を取得
 - 再生中は再生楽曲と現在のキューを表示
 - Spotify Premiumユーザーは再生・一時停止、曲戻し、曲送り可能

### My Library
Spotifyのマイライブラリを表示するビュー
 - お気に入りやフォローしたものを表示
 - 楽曲はまとめてフォロー可能（アルバム・プレイリスト・アーティストも同様）

## Documents
機能などをまとめた発表資料は下記リンクから使用できます。

[Chorus プレゼンテーション](chorus.pdf)
