name: Q_Notice12

on:
  schedule:
    - cron: '*/20 * * * * '
  watch:
    types: [started]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v2
        
      - name: 'Set up Python'
        uses: actions/setup-python@v1
        with:
          python-version: 3.7
         
      - name: 'Install requirements'
        run: pip install -r ./Q_sub/requirements.txt 
        
      - name: '公众号iosrule' 
        run: python3 ./Q_sub/Q_Notice12.py
        env:
            DJJ_BARK_COOKIE: ${{ secrets.DJJ_BARK_COOKIE }}
            DJJ_SEVER_JIANG: ${{ secrets.DJJ_SEVER_JIANG }}
            ios_wturl: ${{ secrets.ios_wturl }}
            ios_newhd: ${{ secrets.ios_newhd }}
            ios_newbt: ${{ secrets.ios_newbt }}
