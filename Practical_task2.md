1. Do some research on the Python requests module. Explain what it is, and how it is used to make HTTP requests.

The Python requests module is a library used to send HTTP requests from a Python program to websites or web servers. After researching it, I understood that it works like a simple way for Python to communicate with web APIs or online services without needing to manually handle low-level network details.

When a program uses requests, it can send different types of HTTP requests such as:
- GET → used to retrieve data from a server
- POST → used to send data to a server
- PUT → used to update data
- DELETE → used to remove data

The module makes this easier because the developer only needs a few lines of code. For example, a GET request can be done by writing something like requests.get(url) and then reading the response.

The response usually includes:
- Status code (example: 200 = success)
- Response data
- Headers
- Content returned by the server

In practice, this module is commonly used when:
- Fetching data from APIs
- Sending form data
- Integrating with external services
- Testing web endpoints

One of the main things I noticed during research is that requests hides a lot of complexity and makes HTTP communication easier to understand.

2. Document your independent fi ndings on the JSON and XML data formats and what they are used for. List at least four advantages and four disadvantages of each data format.

JSON (JavaScript Object Notation) is a text format used for storing and exchanging data. It is based on key–value pairs and looks similar to Python dictionaries.
JSON is widely used when APIs send data between systems because it is lightweight and easy to read.

Example of JSON:
{
  "name": "Product",
  "price": 10
}

Advantages of JSON
- Easy for humans to read and write
- Smaller file size compared to XML
- Works naturally with JavaScript and modern web applications
- Simple structure makes parsing fast and easy

Disadvantages of JSON
- Does not support comments inside files
- Less strict structure validation compared to XML
- Not ideal for very complex hierarchical data
- Limited support for metadata

XML (Extensible Markup Language) is another format used to store and transfer data. It uses tags, similar to HTML, to describe data.

Example of XML:
<product>
    <name>Product</name>
    <price>10</price>
</product>

XML is older than JSON and is still used in some enterprise systems and configuration files.

Advantages of XML
- Very structured and well organised
- Supports validation through schemas
- Good for complex or nested data
- Can include metadata and attributes

Disadvantages of XML
- More verbose (larger file sizes)
- Harder to read compared to JSON
- Parsing is usually slower
- Requires more code to work with

3. Provide a brief explanation of what a RESTful API is, how it works and what it is used for. List at least four advantages and four disadvantages of RESTful APIs.

A RESTful API is a way for different software systems to communicate with each other using HTTP requests. REST stands for Representational State Transfer.

After researching it, I understood that a REST API works by exposing resources (such as users or products) through URLs. Each resource can be accessed using standard HTTP methods:

- GET → read data
- POST → create data
- PUT → update data
- DELETE → remove data

For example:
/products
/products/1

These endpoints allow applications to send and receive data, usually in JSON format.

RESTful APIs are used for:
- Connecting frontend and backend systems
- Mobile applications communicating with servers
- Integrating external services
- Sharing data between systems

Advantages of RESTful APIs
- Simple and easy to understand
- Uses standard HTTP methods
- Scalable for large systems
- Works with many different programming languages

Disadvantages of RESTful APIs
- Can require multiple requests for complex data
- No strict standard enforcement (implementation may vary)
- Over-fetching or under-fetching data can happen
- Requires good documentation to use correctly