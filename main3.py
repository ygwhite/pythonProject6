from yoomoney import Authorize

Authorize(
      client_id="DB09B8E9C9B4310BA9AACE33B89BB3B0114AA7906F30D318A2840A23EBC13DA8",
      redirect_uri="YOUR_REDIRECT_URI",
      scope=["account-info",
             "operation-history",
             "operation-details",
             "incoming-transfers",
             "payment-p2p",
             "payment-shop",
             ]
      )
