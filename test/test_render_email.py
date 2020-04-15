from app.shopping_cart import render_email, beginning_time, to_usd

def test_render_email():
    html = "<div>"
    html +="<br>"
    html +=" Cagney's Corner Shop<br>"
    html +=" www.Cagneys-corner-shop.com<br>"
    html +="<br>"
    html +=" CHECKOUT AT: " + beginning_time + "<br>"
    html +="<br>"
    html +=" SELECTED PRODUCTS:<br>"
    html +="<br>"
    html +=" SUBTOTAL: $4.00<br>"
    html +=" TAX: $1.00<br>"
    html +=" TOTAL: $5.00<br>"
    html +=" Please come again!<br>"
    html +="</div>"
    rendered = render_email([], 4, 1, 5, beginning_time)
    assert rendered == html