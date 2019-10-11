# StockProject

## How to run?

**1. Build docker image and run**

The first time you clone files, run the command written below.
```bash
docker build ./ -t stockproject 
docker run -v $PWD:/usr/work -it --name stockproject stockproject sh
```

From the second time, run the command written below.
```bash
docker start stockproject
docker exec -i -t stockproject sh
```


**2. First you have to scrape current stock price.*  *
```bash
cd src
python stockprice_scraper.py
```


**3. Now you can run line bot.**  
```bash
python run.py
```


## References

- trade data  
https://225labo.com/modules/download/
- definition of traiding day  
https://www.jpx.co.jp/derivatives/rules/night-session/index.html
- definition of RSI  
https://faq.rakuten-sec.co.jp/faq_detail.html?id=1102025


