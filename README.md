# Seven-Eleven Naama Jashin Crawler
A tool to make sure you want this "Naama Jashin".

## Usage
> [!IMPORTANT]  
> This tool use Python 3.11 and poetry.  
> Please make sure you have the environment before using it.  

1. Install Python 3.11 and poetry
2. Install package
```shell
$ poetry install
```
3. Copy `request.json.example` to `request.json`
```shell
cp request.json.example request.json
```
4. Fill the `request.json`
5. Run
```shell
$ poetry shell
$ python3 main.py
```

## Format of `request.json`
```json
[
  {
    "name": "...", 
    "url": "...",
    "requested_id": ["..."]
  }
]
```
`name`: This field will not be used in the tool, only for you to make sure you do not write wrong in json file.  
`url`: This field is the target url to crawl. It should be started with "https://www.sej.co.jp/products/bromide/".  
`requested_id`: This is a list of "予約番号"。  

## Notice
The purpose of this tool is to confirm whether the desired Naama Jashin is correct. Please do not use it for other purposes.