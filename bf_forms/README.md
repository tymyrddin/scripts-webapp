# Brute-Forcing WP HTML form authentication

A simple brute forcer that will be useful against WordPress. Modern WordPress systems include some basic anti-brute-force techniques, but still lack account lockouts or strong captchas by default.

The tool meets two requirements: 
* It retrieves the hidden token from the login form before submitting the password attempt
* It ensures accepting cookies in the HTTP session