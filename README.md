# citbike

CitiBike - visualizations and classification of usertypes (Subscribers vs. Customers)

- 882 station ids
- 17902231 trips
- 89.26% subscribers

## Getting Started

### Fetch data

Fetch the citibike data from the [official S3 container](https://s3.amazonaws.com/tripdata/index.html) with:

```python
python ./src/io.py
```

The data is written into the `trips` table of a `sqlite` database with the following column names:

- tripduration
- starttime, stoptime
- start_id, start_name,start_lat,start_lon
- end_id,end_name,end_lat,end_lon
- bikeid
- usertype
- birth_year
- gender

### Maps API

You need a valid GoogleMaps API key.

## Website Deployment

The website/presentation of this project is hosted on github pages. The `reveal.js` presentation can be generated with the following command:

```shell
pandoc --mathjax -t revealjs -s -o docs/index.html docs/presentation.md \
--css=www/custom.css \
--slide-level=3 \
--highlight-style=breezeDark \
-V revealjs-url=https://revealjs.com \
-V theme=night \
-V progress=true \
-V slideNumber=true \
-V hash=true \
-V navigationMode=linear \
-V transition='slide'
```

## Built With

- [reveal.js](https://github.com/hakimel/reveal.js)
- [pandas](https://github.com/pandas-dev/pandas)
- [boto3](https://github.com/boto/boto3)
- [folium](https://github.com/python-visualization/folium)
- [googlemaps](https://github.com/googlemaps/google-maps-services-python)
- [pandoc](https://pandoc.org/)
- [scikit-learn](https://github.com/scikit-learn/scikit-learn)
- [citibike public data](https://www.citibikenyc.com/data-sharing-policy)
- [plotly](https://github.com/plotly/plotly.py)

## License

The content of the presentation and the content of the website for this project are licensed under the [Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). The underlying source code is licensed under the MIT license.
