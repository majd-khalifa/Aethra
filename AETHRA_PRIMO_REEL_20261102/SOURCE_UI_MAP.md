# Source-verified Primo UI reconstruction

> Production is STOPPED. The current family character designs/illustration style are REJECTED. This source mapping and verified original UI assets are preserved as useful references; the reconstructed commercial is not approved. See `../PRODUCTION_HANDOFF.md`.

All app UI in the final commercial is a **React/Remotion reconstruction**, not an authenticated capture, and not a running Flutter app. This is the user's explicitly authorized fallback. The on-screen app segment carries an Arabic reconstruction/demo-data disclosure. No real order is submitted. No credentials, customer details, API endpoints or tokens are included in the video or its editable UI data.

Read-only reference root: `D:\MAJD Files\Projects\Collage Projects\Production_Ready_Projects\Primo\frontend\Primo`.

| Original screen / component | Reference beneath `lib/` | Treatment in commercial |
|---|---|---|
| Home | `feature/home/presentation/screen/home.dart` | Reconstructed header, search, category carousel and latest-product grid. No fictional home-page add buttons. |
| Categories | `feature/categories/presentation/screen/all_categories_screen.dart`; `feature/home/presentation/widgets/catigory_section.dart`; `catigory_chip.dart` | Category carousel is shown on Home. Standalone category screen identified in source but not included in four-second montage. |
| Products in category | `feature/categories/presentation/screen/category_products_screen.dart`; `feature/search/presentation/widgets/user_product_card.dart` | Standalone category grid identified but not shown; the montage browses Home's original two-column latest-product cards from `feature/home/presentation/widgets/product_card.dart`. |
| Product Details | `feature/product/presentation/screen/product_details.dart` | Reconstructed image, title/price, optional note, availability/SKU, description, quantity and actual “أضف إلى السلة” action. |
| Cart | `feature/cart/presentation/screens/cart.dart`; `presentation/widgets/cart_item_card.dart`; `core/widgets/custom_counter.dart` | Reconstructed two-item cart, quantity control, total and “متابعة للدفع”. |
| Checkout | `feature/orders/presentation/screens/checkout.dart`; `presentation/widgets/delivery_method_card.dart`; `summary_row.dart` | Reconstructed delivery/store-pickup cards, safe demonstration address, summary and “تأكيد الطلب”. No invented payment selector. |
| Order confirmation | `feature/orders/presentation/screens/checkout.dart` success listener; `feature/orders/presentation/screens/order_history_screen.dart`; `presentation/widgets/order_history_card.dart`; `core/helper/snack_bar_helper.dart` | Source has **no dedicated confirmation screen**. On success it routes to order history and displays “تم تأكيد الطلب بنجاح!”. This is reconstructed as a demo order-history card plus the source's green success snackbar. |
| Navigation | `core/routing/app_routes.dart`; `feature/main_layout/widgets/floating_circular_nav_bar.dart` | Actual Home → Product Details → Cart → Checkout → Order History progression; the source's five-position navigation with raised red central widgets button. |
| Theme | `core/utils/appcolor/app_colors.dart`; `core/utils/apptextstyle/app_text_style.dart` | `#BB0013` primary, `#F9F9F9` background, `#1A1C1C` text, `#E2E2E2` borders, `#E6BDB8` quantity controls. Cairo weights 400/500/600/700. |
| Imagery / icons | `assets/images/`; `assets/fonts/`; existing release asset `build/app/intermediates/assets/release/mergeReleaseAssets/flutter_assets/fonts/MaterialIcons-Regular.otf` | Original product/category images and fonts copied byte-for-byte into AETHRA. Existing icon font was only read/copied; no build executed. Icon glyph codes resolved from Flutter's Material icon definitions. |

## Data and fidelity limits

Two fictional groceries are used: بندورة (10,000 ل.س) and زيت نباتي (25,000 ل.س). Fictional delivery fee is 5,000 ل.س, fictional total 40,000 ل.س. These are visual demonstration values, **not verified current prices, inventory, fees or an actual offer**. `DEMO` order/SKU and an explicitly fictional address replace any identifying data. No account, phone, production address, real order number or payment data is used.

The presentation is adapted from Flutter to browser layout at the source's 390 × 884.76 design coordinate size. It preserves hierarchy, original text, colors, font assets, imagery and source-supported controls. It is not a claim of pixel identity to a device screenshot. The phone housing, animated touch rings and montage transitions are commercial artwork, not Primo features. The four-second montage compresses customer actions for storytelling.

`src/PrimoUI.tsx` owns the editable reconstruction and safe demo content. `qa/recreated-ui-assets.json` records original asset hashes. `qa/local-reference-before.json` records the read-only baseline; the final verification checks those same files remain unchanged. No screenshot from the earlier login investigation is used in the finished commercial.
