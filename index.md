# SHORTURL API

Create a shortened URL from an original URL and retrieve an original URL from a shortened URL.

## Accepted Methods
  
`GET` | `POST`

- `GET` - Fetches data including both URLs; based on **_short URL_**.
- `POST` - Fetches data including both URLs; based on **_original URL_**.

## `Content-Type` Header

`CURL` and Python `Requests` library do not require passing of the `Content-Type` header.
If using AJAX, one of the following `Content-Type` headers must be used:

- `'Content-Type: application/json'`
- `'Content-Type: text/plain'`

_**Note:** you will need to pass along valid JSON data with them as well. Please see example below._

## URI structure

**ShortURL API** follows `REST` standards by letting the `HTTP` **_method_** passed to it determine what
**_action_** the API needs to take. _Make sure to pass the correct URL version with the chosen action._

`GET` format:

```bash
http://shortu.rl/shorturl/v1/shorturl/v1/<SHORT_URL>
```

`POST` format:

```bash
http://shortu.rl/shorturl/v1/shorturl/v1/<ORIGINAL_URL>
```
  
## Success Response
  
A successful response will yield a standard [HTTP status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) along with the following data in `JSON` format for both `GET` and `POST`:

`HTTP status code`

_AND_

- `short_url` - This is the shortened URL created by the **ShortURL API**
- `original_url` - This is the original URL given to the **ShortURL API**
- `created` - This is the date the `short_url` was created (format: `yyyy-mm-dd hh:mm:ss`)
- `status` - Tells if the request is `OK`, `MODIFIED`, or an `ERROR`

**Example:**

* **Code:** 200 <br />
    **Content:**
    
    ```bash
    {
        'short_url': 'http://shortu.rl/qM',
        'original_url': 'http://example.com/hello-there/testing',
        'created': '2017-01-05 02:57:10.366',
        'status': 'OK'
    }
    ```
 
## Error Response

An error response will yield a standard [HTTP status code](https://en.wikipedia.org/wiki/List_of_HTTP_status_codes) along with the following data in `JSON` format for both `GET` and `POST`:

`HTTP status code`

_AND_

- `code` - This is the HTTP status code
- `error` - This is the message passed back (details in **Error Codes** section below)
- `status` - Tells if the request is `OK`, `MODIFIED`, or an `ERROR`

**Example:**

* **Code:** 400 <br />
    **Content:**
    
    ```bash
    {
        'code': 400,
        'error': 'ERROR_MALFORMED_REQUEST',
        'status': 'ERROR'
    }
    ```

## Status Codes

- `OK` - Everything is "a ok"
- `MODIFIED` - Something in the URL was modified for security (certain characters to HTML-safe sequences)
- `ERROR` - There was an error so processing was stopped (includes description for free)

## Error Codes

| Error | HTTP Status Code | Description |
| --- | --- | --- |
| `ERROR_SHORT_URL_MALFORMED` | `400` | The `short_url` parameter value is not complete (or malformed in some way) |
| `ERROR_INCORRECT_OR_MISSING_PARAM` | `400` | Missing the parameter value or the entire parameter altogether |
| `ERROR_URL_DATA_NOT_PROCESSED` | `400` | Could not process the `original_url` |
| `ERROR_ORIGINAL_URL_NOT_FOUND` | `404` | Could not find data based on given `short_url` |
| `ERROR_URL_DATA_NOT_FOUND` | `404` | Could not find data even though it should be there (_internal error_) |

If you pass in an incorrect base URL, then you will only receive an HTTP status code (no JSON formatted **Error**).

| HTTP Status Code | Description |
| --- | --- |
| `400` | Missing both version number and basename (e.g. missing `/shorturl/v1/`) |
| `405` | Missing version number (e.g. missing `/v1/`) or basename (e.g. missing `/shorturl/`) |
| `405` | Method not allowed (see **Accepted Methods** above) |

## Sample Calls

**CURL**

- **Successful `GET`**

```bash
$ curl "http://shortu.rl/shorturl/v1?short_url=http://shortu.rl/rQ"
{"created": "2017-01-08 05:20:15.320", "original_url": "http://example.com/", "status": "OK", "short_url": "http://shortu.rl/rQ"}
```

- **Successful `GET` (_with **multiple** params in `original_url`_)**
    - _**Note:** If you use the standard `-d` command, CURL will strip everything after the `&` so be sure to use the `--data-urlencode` option instead._

```bash
$ curl http://shortu.rl/shorturl/v1 --data-urlencode "original_url=http://www.somedomain.com/long/url/test/2?params=test&something=other"
```

- **Successful `POST`**

```bash
$ curl http://shortu.rl/shorturl/v1 -d "original_url=http://www.somedomain.com/long/url/test"string/?param=testing&another=yep'})
{"created": "2017-01-08 07:33:07.094", "original_url": "http://www.somedomain.com/long/url/test", "status": "OK", "short_url": "http://shortu.rl/rY"}
```

**Python `Requests` Library:**

```bash
    >>> import requests
    >>> s = requests.Session()
```

- **Successful `GET`**

```bash
>>> r = s.get('http://shortu.rl/shorturl/v1', params={'short_url': 'http://shortu.rl/rQ'})
>>> r.status_code, r.json()
(200, {'created': '2017-01-08 05:20:15.320', 'short_url': 'http://shortu.rl/rQ', 'original_url': 'http://example.com/', 'status': 'OK'})
```

- **Successful `POST`**

```bash
>>> r = s.post('http://shortu.rl/shorturl/v1', params={'original_url': 'http://www.somedomain.com/this/long/url/'})
>>> r.status_code, r.json()
(200, {'created': '2017-01-08 07:57:35.655', 'short_url': 'http://shortu.rl/r0', 'original_url': 'http://www.somedomain.com/this/long/url/', 'status': 'OK'})
```

- **Failed `GET`/`POST` (`POST` shown. _missing `shorturl` in URI_)**
    - _**Note:** r.text used here instead of r.json() - avoids json decoding error_

```bash
>>> r = s.post('http://shortu.rl/v1', params={'original_url': 'http://www.somedomain.com/this/long/url/'})
>>> r.status_code, r.text
(404, '')
```

- **Failed `POST` (_incorrect `<original_url>`_)**
    
```bash
>>> r = s.post('http://shortu.rl/shorturl/v1', params={'original_url': ''})
>>> r.status_code, r.json()
(400, {'error': 'ERROR_INCORRECT_OR_MISSING_PARAM', 'code': 400, 'status': 'ERROR'})
```

- **Failed `GET` (_incorrect `<short_url>`_)**
    
```bash
>>> r = s.get('http://shortu.rl/shorturl/v1', params={})
>>> r.status_code, r.json()
(400, {'error': 'ERROR_INCORRECT_OR_MISSING_PARAM', 'code': 400, 'status': 'ERROR'})
```

**AJAX (jQuery):**

- **`POST`**

```javascript
jQuery( function($) {
    params = {'original_url': 'http://somelongurl.com/with/all/this/stuff'}
    json_params = JSON.stringify(params)
    $.ajax({
        url: 'http://localhost:8080/shorturl/v1',
        type: 'POST',
        contentType: 'application/json',  // contentType must be supplied (see above)
        data: json_params  // must supply valid JSON
    }).done(function(data) {
        // do stuff
    }).fail(function(jqXHR, statusText, errorThrown) {
        // do stuff
    });
});
```

- **`GET`**

```javascript
jQuery( function($) {
    params = {'short_url': 'http://shortu.rl/rQ'}
    json_params = JSON.stringify(params)
    $.ajax({
        url: 'http://localhost:8080/shorturl/v1',
        type: 'GET',
        contentType: 'text/plain',  // contentType must be supplied (see above)
        data: json_params  // must supply valid JSON
    }).done(function(data) {
        // do stuff
    }).fail(function(jqXHR, statusText, errorThrown) {
        // do stuff
    });
}); 
```


## Rate Limited

The **ShortURL API** is currently rate limited to two (2) requests per second.

## Note to Developers

It may seem that having to pass `http://shortu.rl/shorturl/v1` in (say, rather than just `http://shortu.rl/v1`) is redundant
but keep in mind that the **ShortURL API** is part of a suite of APIs offered by **shortu.rl**.

## Roadmap

- Add unit testing
- Add a front-end website for the ShortURL API
- Add API keys for tracking purposes - if Oauth1.0a will be a while
- Add authorization via Oauth1.0a - TBD
- Add Analytics
