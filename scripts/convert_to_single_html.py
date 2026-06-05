#!/usr/bin/env python3
import re
import sys
from pathlib import Path

CDN = "https://cloud.cdn.almacen.paulinacocina.net/public"
GCS_UPLOADS = "https://almacen-wordpress-prod-media-bz.storage.googleapis.com/wp-content/uploads"
WP = "https://almacen.paulinacocina.net/wp-content"
WP_INCLUDES = "https://almacen.paulinacocina.net/wp-includes"
WP_PLUGINS = f"{WP}/plugins"
WP_THEMES = f"{WP}/themes"
WP_UPLOADS_ELEMENTOR = f"{WP}/uploads/elementor/css"
WP_GOOGLE_FONTS = f"{WP}/uploads/elementor/google-fonts/css"
ELEMENTOR = f"{WP_PLUGINS}/elementor"
ELEMENTOR_PRO = f"{WP_PLUGINS}/elementor-pro"
WC = f"{WP_PLUGINS}/woocommerce"
WC_MEMBERSHIPS = f"{WP_PLUGINS}/woocommerce-memberships"
WC_MULTI = f"{WP_PLUGINS}/woocommerce-multi-currency"
WC_STRIPE = f"{WP_PLUGINS}/woocommerce-gateway-stripe"
WC_PAYPAL = f"{WP_PLUGINS}/woocommerce-paypal-payments"
HELLO_THEME = f"{WP_THEMES}/hello-elementor/assets"
MARKET_THEME = f"{WP_THEMES}/market_paulina"
MAILCHIMP = f"{WP_PLUGINS}/mailchimp-for-woocommerce"
GTM4WP = f"{WP_PLUGINS}/duracelltomi-google-tag-manager"
EEC = f"{WP_PLUGINS}/enhanced-e-commerce-for-woocommerce-store"
AFFILIATE_WP = f"{WP_PLUGINS}/affiliate-wp"
WOO_PB = f"{WP_PLUGINS}/woo-product-bundle"
BEROCKET = f"{WP_PLUGINS}/advanced-product-labels-for-woocommerce"
AREA_MEMBRESIAS = f"{WP_PLUGINS}/area_membresias"
NSL = f"{WP_PLUGINS}/nextend-facebook-connect"


CSS_MAP = {
    # Elementor core
    "frontend.min.css": f"{ELEMENTOR}/assets/css/frontend.min.css",
    "apple-webkit.min.css": f"{ELEMENTOR}/assets/css/conditionals/apple-webkit.min.css",
    "popup.min.css": f"{ELEMENTOR_PRO}/assets/css/conditionals/popup.min.css",
    "sticky.min.css": f"{ELEMENTOR_PRO}/assets/css/modules/sticky.min.css",
    # Elementor widgets
    "widget-counter.min.css": f"{ELEMENTOR}/assets/css/widget-counter.min.css",
    "widget-divider.min.css": f"{ELEMENTOR}/assets/css/widget-divider.min.css",
    "widget-heading.min.css": f"{ELEMENTOR}/assets/css/widget-heading.min.css",
    "widget-icon-box.min.css": f"{ELEMENTOR}/assets/css/widget-icon-box.min.css",
    "widget-image.min.css": f"{ELEMENTOR}/assets/css/widget-image.min.css",
    "widget-nested-accordion.min.css": f"{ELEMENTOR}/assets/css/widget-nested-accordion.min.css",
    "widget-social-icons.min.css": f"{ELEMENTOR}/assets/css/widget-social-icons.min.css",
    "widget-form.min.css": f"{ELEMENTOR_PRO}/assets/css/widget-form.min.css",
    "widget-login.min.css": f"{ELEMENTOR_PRO}/assets/css/widget-login.min.css",
    "widget-mega-menu.min.css": f"{ELEMENTOR_PRO}/assets/css/widget-mega-menu.min.css",
    "widget-nav-menu.min.css": f"{ELEMENTOR_PRO}/assets/css/widget-nav-menu.min.css",
    "widget-woocommerce-menu-cart.min.css": f"{ELEMENTOR_PRO}/assets/css/widget-woocommerce-menu-cart.min.css",
    # Elementor animations
    "fadeIn.min.css": f"{ELEMENTOR}/assets/lib/animations/styles/fadeIn.min.css",
    "fadeInLeft.min.css": f"{ELEMENTOR}/assets/lib/animations/styles/fadeInLeft.min.css",
    "fadeInRight.min.css": f"{ELEMENTOR}/assets/lib/animations/styles/fadeInRight.min.css",
    # Font Awesome (Elementor)
    "all.min.css": f"{ELEMENTOR}/assets/lib/font-awesome/css/all.min.css",
    "v4-shims.min.css": f"{ELEMENTOR}/assets/lib/font-awesome/css/v4-shims.min.css",
    # Hello Elementor theme
    "reset.css": f"{HELLO_THEME}/css/reset.css",
    "theme.css": f"{HELLO_THEME}/css/theme.css",
    "header-footer.css": f"{HELLO_THEME}/css/header-footer.css",
    # Market Paulina (child theme)
    "style.css": f"{MARKET_THEME}/style.css",
    # WooCommerce
    "woocommerce-layout.css": f"{WC}/assets/css/woocommerce-layout.css",
    "woocommerce-smallscreen.css": f"{WC}/assets/css/woocommerce-smallscreen.css",
    "woocommerce.css": f"{WC}/assets/css/woocommerce.css",
    "woocommerce-notices.min.css": f"{ELEMENTOR_PRO}/assets/css/woocommerce-notices.min.css",
    "wc-blocks.css": f"{WC}/assets/client/blocks/wc-blocks.css",
    # WooCommerce Memberships
    "wc-memberships-blocks.min.css": f"{WC_MEMBERSHIPS}/assets/css/blocks/wc-memberships-blocks.min.css",
    "wc-memberships-frontend.min.css": f"{WC_MEMBERSHIPS}/assets/css/frontend/wc-memberships-frontend.min.css",
    # WooCommerce Multi-Currency
    "woocommerce-multi-currency.min.css": f"{WC_MULTI}/css/woocommerce-multi-currency.min.css",
    # Stripe & PayPal
    "upe-blocks.css": f"{WC_STRIPE}/build/upe-blocks.css",
    "ppcp-local-alternative-payment-methods-css-gateway.css": f"{WC_PAYPAL}/assets/ppcp-local-alternative-payment-methods-css-gateway.css",
    # Woo Product Bundle
    "blocks.css": f"{WOO_PB}/assets/css/blocks.css",
    "frontend.css": f"{WOO_PB}/assets/css/frontend.css",
    # Mailchimp
    "style-sms-consent-block.css": f"{MAILCHIMP}/blocks/build/style-sms-consent-block.css",
    # Membership
    "membership-styles.css": f"{AREA_MEMBRESIAS}/membership-styles.css",
    # Berocket labels
    "font-awesome.min.css": f"{BEROCKET}/berocket/assets/css/font-awesome.min.css",
    # AffiliateWP
    "forms.min.css": f"{AFFILIATE_WP}/assets/css/forms.min.css",
    # wp-includes
    "style.min.css": f"{WP_INCLUDES}/css/dist/block-library/style.min.css",
    # Google Fonts (Elementor)
    "inter.css": f"{WP_GOOGLE_FONTS}/inter.css",
    "montserrat.css": f"{WP_GOOGLE_FONTS}/montserrat.css",
    "nunito.css": f"{WP_GOOGLE_FONTS}/nunito.css",
    "nunitosans.css": f"{WP_GOOGLE_FONTS}/nunitosans.css",
}

# Duplicate files: Chrome renames when names collide.
# Map the Chrome-generated name to its actual original filename.
CSS_DUPLICATES = {
    "frontend(1).css": "frontend.css",
}

CSS_ADDITIONAL = {
    "frontend.css": f"{BEROCKET}/css/frontend.css",
}

# Elementor post-specific CSS
CSS_POST_BASE = f"{WP_UPLOADS_ELEMENTOR}"

JS_MAP = {
    # jQuery (from WP includes)
    "jquery.min.js": f"{WP_INCLUDES}/js/jquery/jquery.min.js",
    "jquery-migrate.min.js": f"{WP_INCLUDES}/js/jquery/jquery-migrate.min.js",
    "jquery-3.6.0.min.js": "https://code.jquery.com/jquery-3.6.0.min.js",
    # jQuery UI
    "core.min.js": f"{WP_INCLUDES}/js/jquery/ui/core.min.js",
    # jsPDF
    "jspdf.umd.min.js": "https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js",
    # Elementor core
    "webpack.runtime.min.js": f"{ELEMENTOR}/assets/js/webpack.runtime.min.js",
    "frontend-modules.min.js": f"{ELEMENTOR}/assets/js/frontend-modules.min.js",
    "frontend.min.js": f"{ELEMENTOR}/assets/js/frontend.min.js",
    "jquery-numerator.min.js": f"{ELEMENTOR}/assets/lib/jquery-numerator/jquery-numerator.min.js",
    "v4-shims.min.js": f"{ELEMENTOR}/assets/lib/font-awesome/js/v4-shims.min.js",
    # Elementor Pro
    "webpack-pro.runtime.min.js": f"{ELEMENTOR_PRO}/assets/js/webpack-pro.runtime.min.js",
    "frontend.min(1).js": f"{ELEMENTOR_PRO}/assets/js/frontend.min.js",
    "elements-handlers.min.js": f"{ELEMENTOR_PRO}/assets/js/elements-handlers.min.js",
    "jquery.smartmenus.min.js": f"{ELEMENTOR_PRO}/assets/lib/smartmenus/jquery.smartmenus.min.js",
    "jquery.sticky.min.js": f"{ELEMENTOR_PRO}/assets/lib/sticky/jquery.sticky.min.js",
    # Elementor Pro (non-minified)
    "frontend.js": f"{ELEMENTOR_PRO}/assets/js/frontend.js",
    # Hello theme
    "hello-frontend.js": f"{HELLO_THEME}/js/hello-frontend.js",
    # WooCommerce
    "add-to-cart.min.js": f"{WC}/assets/js/frontend/add-to-cart.min.js",
    "cart-fragments.min.js": f"{WC}/assets/js/frontend/cart-fragments.min.js",
    "geolocation.min.js": f"{WC}/assets/js/frontend/geolocation.min.js",
    "woocommerce.min.js": f"{WC}/assets/js/frontend/woocommerce.min.js",
    "jquery.blockUI.min.js": f"{WC}/assets/js/jquery-blockui/jquery.blockUI.min.js",
    "jquery.cookie.min.js": f"{WC}/assets/js/jquery-cookie/jquery.cookie.min.js",
    "js.cookie.min.js": f"{WC}/assets/js/js-cookie/js.cookie.min.js",
    "selectWoo.full.min.js": f"{WC}/assets/js/selectWoo/selectWoo.full.min.js",
    # WooCommerce Multi-Currency
    "woocommerce-multi-currency.min.js": f"{WC_MULTI}/js/woocommerce-multi-currency.min.js",
    "woocommerce-multi-currency-switcher.min.js": f"{WC_MULTI}/js/woocommerce-multi-currency-switcher.min.js",
    # WooCommerce Memberships
    "wc-memberships-blocks-common.min.js": f"{WC_MEMBERSHIPS}/assets/js/frontend/wc-memberships-blocks-common.min.js",
    # Woo Product Bundle
    "frontend.js": f"{WOO_PB}/assets/js/frontend.js",
    # Mailchimp
    "mailchimp-woocommerce-public.min.js": f"{MAILCHIMP}/public/js/mailchimp-woocommerce-public.min.js",
    "mailchimp-woocommerce-pixel-tracking.js": f"{MAILCHIMP}/public/js/mailchimp-woocommerce-pixel-tracking.js",
    "pixel-tracking.js": f"{MAILCHIMP}/blocks/build/pixel-tracking.js",
    # GTM4WP / Ecommerce
    "gtm4wp-ecommerce-generic.js": f"{GTM4WP}/dist/js/gtm4wp-ecommerce-generic.js",
    "gtm4wp-woocommerce.js": f"{GTM4WP}/dist/js/gtm4wp-woocommerce.js",
    "con-gtm-google-analytics.js": f"{EEC}/public/js/con-gtm-google-analytics.js",
    # AffiliateWP
    "tracking.min.js": f"{AFFILIATE_WP}/assets/js/tracking.min.js",
    # WP polyfill / hooks / i18n
    "wp-polyfill.min.js": f"{WP_INCLUDES}/js/dist/vendor/wp-polyfill.min.js",
    "hooks.min.js": f"{WP_INCLUDES}/js/dist/hooks.min.js",
    "i18n.min.js": f"{WP_INCLUDES}/js/dist/i18n.min.js",
    # Google / GTM
    "gtm.js": "https://www.googletagmanager.com/gtm.js",
    "js": "https://www.googletagmanager.com/gtag/js",
    "9d5e8f3b18bce027b24299069.js": "https://chimpstatic.com/mcjs-connected/js/users/4e1fd4c6c689d90f6afc30d1c/9d5e8f3b18bce027b24299069.js",
    # Flodesk (universal tracking)
    "universal.mjs": "https://universal.flodesk.com/universal.mjs",
    "universal.js": "https://universal.flodesk.com/universal.js",
    # Dialog (Elementor dependency, loaded dynamically - include anyway)
    "dialog.min.js": f"{ELEMENTOR}/assets/lib/dialog/dialog.min.js",
}

# Map post-specific CSS (post-*.css)
def post_css_url(filename):
    return f"{CSS_POST_BASE}/{filename}"

# Images: CDN for .webp, GCS for logo
def image_url(filename):
    if filename == "logo_textura.png":
        return f"{GCS_UPLOADS}/2023/09/logo_textura.png"
    if filename in ("logo_white.svg", "whatsapp-icon.svg"):
        return f"{CDN}/{filename}"
    return f"{CDN}/{filename}"


def inline_page_css(raw, files_dir):
    """Inline the page-specific Elementor CSS (post-XXXXX.css).
    Returns (raw_with_css_inlined, post_id) where post_id is the page's post ID.
    """
    m = re.search(r'class="elementor elementor-(\d+)"', raw)
    if not m:
        return raw, None
    post_id = m.group(1)
    css_path = Path(files_dir) / f"post-{post_id}.css"
    if not css_path.exists():
        print(f"  ⚠ No se encontró {css_path} para inline", file=sys.stderr)
        return raw, post_id
    css_content = css_path.read_text("utf-8")
    raw = re.sub(
        rf'<link[^>]*href="[^"]*post-{post_id}\.css[^"]*"[^>]*>',
        f'<style id="elementor-post-{post_id}-css">{css_content}</style>',
        raw,
    )
    print(f"  ✅ post-{post_id}.css inlinado ({len(css_content)} chars)")
    return raw, post_id


def convert_file(html_path):
    html_path = Path(html_path)
    raw = html_path.read_text("utf-8")

    # Determine the _files directory name from the HTML path
    files_dir = html_path.stem + "_files"

    # Inline page-specific Elementor CSS before general replacement
    raw, post_id = inline_page_css(raw, files_dir)

    # Escape special regex chars in the directory name
    escaped_dir = re.escape(files_dir)

    def replace_match(m):
        attr = m.group(1)
        fname = m.group(2)

        # Handle .download extension (Chrome adds this for JS files)
        if fname.endswith(".download"):
            fname = fname[:-9]

        # Determine URL based on file type
        if fname.endswith((".webp", ".png", ".svg")):
            url = image_url(fname)
        elif fname.startswith("post-") and fname.endswith(".css"):
            url = post_css_url(fname)
        elif fname in CSS_MAP:
            url = CSS_MAP[fname]
        elif fname in CSS_DUPLICATES:
            original = CSS_DUPLICATES[fname]
            url = CSS_MAP.get(original) or (CSS_ADDITIONAL.get(original) or post_css_url(original))
        elif fname in CSS_ADDITIONAL:
            url = CSS_ADDITIONAL[fname]
        elif fname in JS_MAP:
            url = JS_MAP[fname]
        elif fname.endswith(".css") and fname.startswith("widget-"):
            # Widget CSS from Elementor
            url = f"{ELEMENTOR}/assets/css/{fname}"
        else:
            print(f"  ⚠ Sin mapeo: {fname}", file=sys.stderr)
            return m.group(0)

        return f'{attr}="{url}"'

    result = re.sub(
        rf'(src|href)=["\']\./{escaped_dir}/([^"\']*?)(?:\.download)?["\']',
        replace_match,
        raw,
    )

    html_path.write_text(result, "utf-8")
    print(f"  ✅ {html_path}")


def main():
    if len(sys.argv) < 2:
        print("Uso: python3 scripts/convert_to_single_html.py <ruta/al/archivo.html>", file=sys.stderr)
        sys.exit(1)

    for path in sys.argv[1:]:
        p = Path(path)
        if not p.exists():
            print(f"Error: archivo no encontrado: {p}", file=sys.stderr)
            sys.exit(1)
        print(f"Procesando: {p}")
        convert_file(p)


if __name__ == "__main__":
    main()
