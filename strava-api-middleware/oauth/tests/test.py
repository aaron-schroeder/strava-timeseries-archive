import json

from oauth.domain.model import AccessTokenObject, AccessToken


def test(access_token_dict):
    access_token = AccessToken.from_dict(access_token_dict)
    assert isinstance(access_token, AccessToken)

    access_token_object = AccessTokenObject.from_dict(access_token_dict)
    assert isinstance(access_token_object, AccessTokenObject)

    assert access_token.access_token_object == access_token_object

    print('Tests passed for the following access token dict: \n',
          json.dumps(access_token_dict, indent=4))


loaded_tp_access_token = {
    'athlete': {
        'id': 11111111
    },
    # Format suggests this is a Fernet-encrypted token (starts with `gAAAA`)
    'access_token': 'gAAAAFxNK3bFijaU_o1gygVytFpfChaTbBRi1R44v_H5q4juHiuEorbweT8w-Apv5w9BdUFJ2NH2avZ6btx9tzIcoDlKojWkMj1Tcim24q-njtTzQY-o9lnZNKWWgGALtcuGpqxCDx24-S_C0SQ4Vtdd86BDupjHQyRKSQAS2lt-iLIC1AEAAIAAAAA1iFCPInKyX2QtOuJH4zvnBkwm6ht6q33epb3XZRsC8doGgvejDYX-pG60I_TTpfB6lyWkKHFQ-ZH_gUYRik4c4Q-WoRy2slZj0c_WB9R-eEIGi_eunmO-TBh8K0cZ9JfgGoXkUcxE_Qq4erONAjE9UdSEwjDMJM88xbFVGrvcfxkx3xAWPeA1HZOj9JOj6IY2OT6BMXc8vLTS0g-gh9s43Bjd02xjuJmnXYiB4Nzk8qmIZ7kYlP6d51kBFjQwbZUOcfhTHUaOJoehCRxBR3gEOYgcaG8M32TuzL_U85rwhmmpoRqt_uyCVrz3V2mKhsmI1x7_Mq-FbWlWrIZ1psje30VIecnfGZD42A0AOYJ1WKay4U6QhXK_IUgR-xzS28YCl4I-TvuXtxxoLs2W8UMTO2jDJu4pc8tAKcATYYlP7KM7dk05GuAb0CAbZBa62LgVV_cFDG_xJPGFSG_acGdqqbL0RZ9uF35twEjgx7ySbJ-72UOlJ6bDjlPUpDiCVRPUZ25jjjzlidW3z0FWZszKlAsc1h4Gy_ad1ZDD4oI5OGmScrm_rZpUYkCkZjVunFvrt-v8W2vqbgiF6LKXVzvOC_CwaHn3ynCkjgZ4HUlClg',
    # Could be a custom token format from a commercial auth provider (e.g., OAuth provider like Auth0, Okta, or a private OAuth2 implementation).
    'refresh_token': 'GidM!IAAAAH9Iqhfjdw_K0CPxaHhQvHkY7XBSxxnlWfaZw-TlrpqkQQEAAAGEut0_lsKM3QZx2Z55ihzueoZQfPMHnfAVPoVDIUNhH2gsbZOf83npF4OHj1WGfb0n56ALpySz7TbDUTL7peLFlBCXbBkJz3Zuu9hSAUJHLNnibBixKK-x84Sn-PpdtI9ReG_pX1O7gWM4WoIVEOwuMJ3GxoZxgDUACqy55-fLcN_vQoQIVdJVvsWJJGvZBSjF5dQbgP2Fv6164Ldzs6M_1O4E7HNT0EZ_TDmK4K1GpcBb0Vt2kJNtsO0ZcfecdN2WAKhCjuxuKcIxFQD2Sy39V9JHmRJ5A7bt5DA1mKwihIzOcTxOq1adpvgZTiDzA2wPPSgYB96TPeVaV33VhpSmVPDvGfyU_pKWm0x2z1tHh6W9auEhBZxl4Rs7bZiHvef1gTck9bEQl0qm3o4gREh5VJ0OpWJASMhaqOrh7ffYLA',
    'expires_at': 1745418887,
    'expiration_time': '2025-04-23 14:34:47'
}

test(loaded_tp_access_token)

loaded_strava_access_token = {
    'athlete': {
        'id': 123456789
    },
    # Both tokens look like SHA-1 or 160-bit random hex
    'access_token': '3e25b3b70ca92842d1c8fec1f026f13782c6ad2a',
    'refresh_token': '88580d9668f0934546af193d4b3f8214e99f78d9',
    'expires_at': 1739742921,
    'expiration_time': '2025-02-16 21:55:21'
}

test(loaded_strava_access_token)

print('All tests passed')