name: Sam_youku0

on:
  schedule:
    - cron: '*/15 * * * * '
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
        run: pip install -r ./Sam/requirements.txt 
        
      - name: '公众号iosrule' 
        run: python3 ./Sam/Sam_youku0.py 
        env:
            sam_url: ${{ secrets.sam_url }}
            sam_headers: ${{ secrets.sam_headers }}
            sam_body0: ${{ secrets.sam_body0 }}
