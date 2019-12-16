## Part 1: The data
    The data stored are header, payload and signature.
    Header typically consists of the type of toke and signing algorithm that is 
    used. 
    Payload contains claims, which are the content that we try to store.
    Siganature encode the header, payload and secret then sign that
## Part 2: Justification about tampering
    No. The secret has been modified from "comp1531" to "your-256-bit-secret".
    The siganature "zvYs0A3taZbWJY137oPIw0eAp4sCzNz4F4M6G61fyQE" corresponds the
    secret to "your-256-bit-secret". Tools such as https://jwt.io/ is used to 
    check the data