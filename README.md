# metrics

web
http://vue-metrics.s3-website-ap-northeast-1.amazonaws.com/
api
https://u9ozoz6muk.execute-api.ap-northeast-1.amazonaws.com/Prod?start=-PT1H&end=P0D&type=All

- この機能はなんなのでしょうか？

  - この機能は、AWSのよく使うコンポーネントのメトリクスを一括で取ることができる画面になります。

- どういう時に使いたいか？

  - 新しいプロジェクトに入ってWEBサービスを作ると、最後の方に非機能用件というか、負荷試験とかを頼まれる場合がありますよね。
  - その時に、ただ試験をするのであれば、locustなどを使用して試験をすればいいんですけど、
  - その時にエビデンストとして、サーバーの状態はどうだったか？とか、DBの負荷はどこまで上がっていたか？とかメトリクスを監視する必要があります。
  - MakerelやDataDogを使って収集したりすることもあると思うのですが、
  - AWSにはCloudWatchあるし、最近はContainerInsihgtとかもあるし、
  - 一気に一画面でとれたら楽じゃないかな？という発想から作ってみようと思いました。

- 様式

  ![image](https://user-images.githubusercontent.com/54279162/119360810-f8a49380-bce5-11eb-9b93-60e1c780c6e9.png)

  - s3の静的コンテンツにvuejsのサイト
  - ApiGateWay経由でLambdaの起動
  - Lambda内部でDescribeStackとMetricWidgetImageを使ってデータを返す

  - DescribeStackで取っているので、何も設定しなくてもそれらしきコンポーネントのメトリクス が取れる

- やりたいこと
  - 取れるメトリクスの数を増やす
  - Container Insights の情報をとる(多分取れる)
  - APIの速度を速くする(キャッシュする)

- locust
  - 負荷試験をするために、リクエストを飛ばすツール。
  -  
