
#!/venv/bin
# use source ./setup.sh to execute
export DATABASE_NAME="casting_agency"
export DB_USERNAME="postgres"
export DB_PASSWORD="Test@123"
export DB_HOST="localhost:5432"
export DATABASE_URL="postgresql://${DB_USERNAME}:${DB_PASSWORD}@${DB_HOST}/${DATABASE_NAME}"

# auth variables
export AUTH0_DOMAIN="fsndauthorise.auth0.com"
export ALGORITHMS=['RS256']
export API_AUDIENCE="casting agency"
export CLIENT_ID="WTXUhNAKdJKo2V21uy3V27ibxwzDeURB"
export LOGIN_URL="https://fsndauthorise.auth0.com/authorize?audience=casting%20agency&response_type=token&client_id=WTXUhNAKdJKo2V21uy3V27ibxwzDeURB&redirect_uri=http://localhost:5000/home"

export CASTING_ASSISTANT="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNSmVlYWpMWUNaOXhoRkxUdENRcCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhdXRob3Jpc2UuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlZDdiMzc3NDk4MDRlMGM0YWI3MmNlOCIsImF1ZCI6ImNhc3RpbmcgYWdlbmN5IiwiaWF0IjoxNTkxMjg3NDQ5LCJleHAiOjE1OTEyOTQ2NDksImF6cCI6IldUWFVoTkFLZEpLbzJWMjF1eTNWMjdpYnh3ekRlVVJCIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.Hh-ZUud1cC2nbL_0Vtvy7lcenxqUF1sxkOhYJQYgWu6ig4upWPs0nuNPF5wPydtzh8EzdbKCUr3oEkFl9fVU4AEJHE5l-1ikLob40cWS7LsvLb2zZVJGbZBNkKZeUT1O0LBhaa8ZZ2xA49xWiiWaE7VdcXNPySAhUVpGWJn0QEiSg9LKtPJ8HZLIN3TsdA9Szbf5nJlhQm57Csp7It_A6yjaR0hP-fnL980i5c2CgXr7RhGJTZ4C0fZ0IXR1c9Od3muQ0JDx6Uzf48J178U1OsXpfY0T7Z1qmhr0foeL6TZhe6jfzC5nkttjIciLasmm2s0ZudzNM1xkLlM4tVxglA"
export CASTING_DIRECTOR="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNSmVlYWpMWUNaOXhoRkxUdENRcCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhdXRob3Jpc2UuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlYTY2ZDVmMWNjMWFjMGMxNDY5MzlkMSIsImF1ZCI6ImNhc3RpbmcgYWdlbmN5IiwiaWF0IjoxNTkxMjg4Mjc4LCJleHAiOjE1OTEyOTU0NzgsImF6cCI6IldUWFVoTkFLZEpLbzJWMjF1eTNWMjdpYnh3ekRlVVJCIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIiwicG9zdDptb3ZpZXMiXX0.lTwuQ4VXemJLslNR57NTmFrTq75TEQShHqWUvEBoDizMA7Ho1HbkMAfL2vy5LMraIpaqEFY8lHW4oZQh7zRkPfOaqYHjCaseVzqi3cfA_-PW4JlU9YKzWSEd5e9PtS9oqHvdztgZ8yaQnPP2qCvi12jEI6eFD5OQikJaeokB2Nb3oTTAHVRySm1lOoLwXTXzyuW6LOYbVa0ev81MdeZfYtCAIHZsFiwzqgz7YT86C8GB-_yrWMtBjfucfyCcO8cBDrl3ljWpCyrm2K0yb7dWGXrcakp6uWI_X-O6CurdEumWHsN0IZLuGsAaf_KR6hTXxHO-TJy0tzTv5qIAeS7vlA"
export EXECUTIVE_PRODUCER="Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlBNSmVlYWpMWUNaOXhoRkxUdENRcCJ9.eyJpc3MiOiJodHRwczovL2ZzbmRhdXRob3Jpc2UuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVlOTcxZGU2MTkwNjI1MGMxNGQ4ZWNiNCIsImF1ZCI6ImNhc3RpbmcgYWdlbmN5IiwiaWF0IjoxNTkxMjg4NDQyLCJleHAiOjE1OTEyOTU2NDIsImF6cCI6IldUWFVoTkFLZEpLbzJWMjF1eTNWMjdpYnh3ekRlVVJCIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.W3neG3dlywKIQ0wIEFh8oNQ1ABDV2w-DRQXZs92lUpsudXUMB2VopQ1eJSip_djTT7TA4nyeavk7qRNlz6bKog5X4vunyf5YzmDQF0fqCPRaXRi0gnOhbxPGiZmbLYltxCO4gnvVVe4rjRb0psaaf9dz6g9JKMSCx73ZkQmB_v9ErKqSjVpfd2XdZDoWfbER651-IZ-hUcajuAcr_Go_9NUx_JVhLB0w6__UMHEkoNsDqF_nCZdQWc_-hob4-Y9AHuc3mgB_K_B9OixKivPjfNiKqcdgyaeOrJz1GWeU1djY6mVoYH1Q13FK1eNWfEgI7Awiq1igByPbXFU0b9YurQ"

