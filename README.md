
# 合宿のアプリ候補

- 「庭に猫が来たらslackに通知するアプリ」
- 「全国200の実店舗の売上データからAWSの機能を使って売上予測とETL処理をしてみた」
- 「自然言語処理BERTを使ったネオ芭蕉BOTの復活」
- 「アレクサスキルビルダー取ったんで、アレクサアプリ作ってみる。」
- 「やっぱり、将棋が好き。AIを独自作成してみた」
- 「最近DeFiとか流行っているみたいなんで、Amazon Managed Blockchainを使って、SUPINF Coinを作ってみた」
- 「負荷試験とかやるの面倒なので簡単に行えるツールを作ってみよう」

# metrics

## web  
http://vue-metrics.s3-website-ap-northeast-1.amazonaws.com/  
## api  
https://u9ozoz6muk.execute-api.ap-northeast-1.amazonaws.com/Prod?start=-PT1H&end=P0D&type=All  

### この機能はなんなのでしょうか？

  - この機能は、AWSのよく使うコンポーネントのメトリクスを一括で取ることができる画面になります。

- どういう時に使いたいか？

  - 新しいプロジェクトに入ってWEBサービスを作ると、最後の方に非機能用件というか、負荷試験とかを頼まれる場合がありますよね。
  - その時に、ただ試験をするのであれば、locustなどを使用して試験をすればいいんですけど、
  - その時にエビデンスとして、サーバーの状態はどうだったか？とか、DBの負荷はどこまで上がっていたか？とかメトリクスを監視する必要があります。
  - MakerelやDataDogを使って収集したりすることもあると思うのですが、
  - AWSにはCloudWatchあるし、最近はContainerInsihgtとかもあるし、
  - 一気に一画面でとれたら楽じゃないかな？という発想から作ってみようと思いました。

# 補足 locust

  - 負荷試験をするために、リクエストを飛ばすツール。

![image](https://user-images.githubusercontent.com/54279162/119435628-7b186c00-bd55-11eb-9c34-a41572a75b1b.png)

  - 発送の元となった大橋さんのドキュメントはこちら  
  - ([こちら]https://git.supinf.co/iridge/eca-geopop/blob/master/stress-test-document/201806/high_stresss_report.md)
  
# 様式

  ![image](https://user-images.githubusercontent.com/54279162/119382731-68724880-bcfd-11eb-90db-48d056b9d3f0.png)

  - s3の静的コンテンツにvuejsのサイト
  - ApiGateWay経由でLambdaの起動
  - Lambda内部でDescribeStackとMetricWidgetImageを使ってデータを返す

  - DescribeStackで取っているので、何も設定しなくてもそれらしきコンポーネントのメトリクス が取れる
  - 逆にいうと今は手で登録したコンポーネントは取れない仕様になってしまっている。

- やりたいこと
  - 土日でやっていたのであんまり進んでいない
  - 取れるメトリクスの数を増やす
  - Container Insights の情報をとる(多分取れる)
  - APIの速度を速くする(キャッシュする)

- 思ったこと
  - あまりやりすぎず、slackにメトリクス画像付きでアップするくらいがちょうどいいのでは
  - CloudWatchのダッシュボードでよくない？
  - SUPINFのCfに組み込んでいくのであれば、CloudWatchのダッシュボードを使うのがスマートな気がしました。
  - CloudFormationのアウトプットから、よく使うコンポーネントのよく使うメトリクスを拾って予めダッシュボードを作るCFを作っちゃう

- 今後について
  - さいとう君みたいにおしゃれなFrontを自在に操ってみたい
  - たかし君、まるさんに連絡がつかなくてもAWSの問題を解決してみたい
  - 営業が得意ではないので、別の方法でなんとか社外影響力をだしたい




