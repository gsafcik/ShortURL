# SHORTURL API

Create a shortened URL from an original URL and retrieve an original URL from a shortened URL.

## Accepted Methods
  
`GET` | `POST`

- `GET` - Fetches data including both URLs; based on **_short URL_**.
- `POST` - Fetches data including both URLs; based on **_original URL_**.

## URI structure

**ShortURL API** follows `REST` standards by letting the `HTTP` **_method_** passed to it determine what
**_action_** the API needs to take. _Make sure to pass the correct URL version with the chosen action._

`GET` format:

`/shorturl/v1/<SHORT_URL>`

`POST` format:

`/shorturl/v1/<ORIGINAL_URL>`
  
## Success Response
  
A successful response will yield the following data in `JSON` format 
for both `GET` and `POST`:

- `short_url` - This is the shortened URL created by the **ShortURL API**
- `original_url` - This is the original URL given to the **ShortURL API**
- `created` - This is the date the `short_url` was created (format: `yyyy-mm-dd hh:mm:ss`)

**Example:**

* **Code:** 200 <br />
    **Content:**
    
    ```bash
    {
        'short_url': 'http://shortu.rl/qM',
        'original_url': 'http://example.com/hello-there/testing',
        'created': '2017-01-05 02:57:10.366'
    }
    ```
 
## Error Response

TBD

## Sample Call

**CURL**

TBD

**Python `Requests` Library:**

```bash
>>> import requests
>>> s = requests.Session()
```

- **Successful `GET`**

    ```bash
    >>> r = s.get('http://shortu.rl/shorturl/v1', params={'short_url': 'http://shortu.rl/rc'})
    >>> r.status_code, r.text
    (200, '{"short_url": "http://shortu.rl/rc", "original_url": "http://www.somedomain.com/this/long/url/string/?param=testing&another=yep", "created": "2017-01-05 11:24:08.519"}')
    ```

- **Successful `POST`**

    ```bash
    >>> r = s.post('http://shortu.rl/shorturl/v1', params={'original_url': 'http://www.somedomain.com/this/long/url/string/?param=testing&another=yep'})
    >>> r.status_code, r.text
    (200, '{"short_url": "http://shortu.rl/rc", "original_url": "http://www.somedomain.com/this/long/url/string/?param=testing&another=yep", "created": "2017-01-05 11:24:08.519"}')
    ```

- **Failed `GET` (_missing `shorturl` in URI_)**

    ```bash
    >>> r = s.get('http://shortu.rl/v1', params={'short_url': 'http://shortu.rl/rc'})
    >>> r.status_code, r.text
    (404, '')
    ```

- **Failed `GET` (_incorrect `<short_url>`_)**
    
    TBD

- **Failed `POST` (_missing `shorturl` in URI_)**
    
    TBD

- **Failed `POST` (_incorrect `<original_url>`_)**
    
    TBD

## Rate Limited

The **ShortURL API** is currently rate limited to two (2) requests per second.

## Note to Developers

It may seem that having to pass `http://shortu.rl/shorturl/v1` in (say, rather than just `http://shortu.rl/v1`) is redundant
but keep in mind that the **ShortURL API** is part of a suite of APIs offered by **shortu.rl**.

## Roadmap

TBD
