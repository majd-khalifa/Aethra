/** Source-verified React reconstruction, NOT a captured/authenticated app.
 * See SOURCE_UI_MAP.md. All displayed product/order/address data are fictional.
 * No API calls, credentials, accounts or live order submission exist here.
 */
import React from "react";
import { Img, staticFile, useCurrentFrame } from "remotion";
import glyphs from "./material-icons.json";
import { ease } from "./Art";
export const P = {
  primary: "#BB0013",
  text: "#1A1C1C",
  bg: "#F9F9F9",
  border: "#E2E2E2",
  grey: "#6B7280",
  brown: "#5D3F3C",
  qty: "#E6BDB8",
};
type IconName = keyof typeof glyphs;
const Icon: React.FC<{ name: IconName; size?: number; color?: string }> = ({
  name,
  size = 26,
  color = P.primary,
}) => (
  <span
    aria-hidden="true"
    style={{
      fontFamily: "Material",
      fontWeight: 400,
      fontSize: size,
      lineHeight: 1,
      direction: "ltr",
      display: "inline-block",
      color,
    }}
  >
    {String.fromCodePoint(glyphs[name])}
  </span>
);
const Text: React.FC<{
  children: React.ReactNode;
  size?: number;
  weight?: number;
  color?: string;
  style?: React.CSSProperties;
}> = ({ children, size = 16, weight = 400, color = P.text, style }) => (
  <div
    style={{
      fontSize: size,
      fontWeight: weight,
      color,
      lineHeight: 1.6,
      ...style,
    }}
  >
    {children}
  </div>
);
const Card: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ children, style }) => (
  <div
    style={{
      background: "#fff",
      border: `1px solid ${P.border}`,
      borderRadius: 16,
      padding: 16,
      ...style,
    }}
  >
    {children}
  </div>
);
const Row: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ children, style }) => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      gap: 8,
      ...style,
    }}
  >
    {children}
  </div>
);
const Gap: React.FC<{ n?: number }> = ({ n = 16 }) => (
  <div style={{ height: n, flexShrink: 0 }} />
);
const Pic: React.FC<{
  file: string;
  width?: number;
  height?: number;
  cover?: boolean;
}> = ({ file, width, height, cover = false }) => (
  <Img
    src={staticFile("primo/" + file)}
    style={{
      width: width ?? "100%",
      height: height ?? "100%",
      objectFit: cover ? "cover" : "contain",
      borderRadius: 8,
    }}
  />
);
const Header: React.FC<{
  title?: string;
  home?: boolean;
  favorite?: boolean;
  plain?: boolean;
}> = ({ title = "Primo", home = false, favorite = false, plain = false }) => (
  <Row style={{ height: 76, flexShrink: 0 }}>
    <Icon
      name={home ? "person" : "arrow_back_rounded"}
      color={home ? P.primary : P.text}
      size={30}
    />
    <Text size={24} weight={700} color={P.primary}>
      {title}
    </Text>
    {plain ? (
      <div style={{ width: 30 }} />
    ) : (
      <Icon
        name={
          favorite ? "favorite_border_outlined" : "notifications_none_rounded"
        }
        size={28}
      />
    )}
  </Row>
);
const Button: React.FC<{ children: React.ReactNode; arrow?: boolean }> = ({
  children,
  arrow = false,
}) => (
  <div
    style={{
      background: P.primary,
      color: "#fff",
      height: 56,
      borderRadius: 16,
      display: "flex",
      alignItems: "center",
      justifyContent: "center",
      gap: 14,
      fontSize: 20,
      fontWeight: 700,
    }}
  >
    {children}
    {arrow && <Icon name="arrow_forward" color="#fff" />}
  </div>
);
const Nav: React.FC<{ active?: "home" | "cart" | "orders" }> = ({
  active = "home",
}) => (
  <div
    style={{
      height: 80,
      position: "absolute",
      bottom: 0,
      left: 0,
      right: 0,
      background: "#fff",
      boxShadow: "0 -2px 10px #00000012",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-around",
    }}
  >
    {(
      [
        { label: "حسابي", icon: "person_outline", a: false },
        { label: "طلباتي", icon: "receipt_long", a: active === "orders" },
        { label: "", icon: "widgets_outlined", a: true },
        {
          label: "السلة",
          icon: "shopping_cart_outlined",
          a: active === "cart",
        },
        { label: "الرئيسية", icon: "home_rounded", a: active === "home" },
      ] as { label: string; icon: IconName; a: boolean }[]
    ).map((item, i) =>
      i === 2 ? (
        <div
          key={i}
          style={{
            width: 65,
            height: 65,
            borderRadius: "50%",
            background: P.primary,
            marginTop: -25,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            boxShadow: "0 4px 12px #BB001360",
          }}
        >
          <Icon name={item.icon} size={32} color="white" />
        </div>
      ) : (
        <div key={i} style={{ textAlign: "center", width: 62 }}>
          <Icon name={item.icon} color={item.a ? P.primary : P.grey} />
          <Text size={12} weight={700} color={item.a ? P.primary : P.grey}>
            {item.label}
          </Text>
        </div>
      ),
    )}
  </div>
);
const Counter: React.FC = () => (
  <div
    style={{
      display: "flex",
      alignItems: "center",
      gap: 16,
      background: P.qty,
      borderRadius: 999,
      padding: "6px 10px",
      direction: "ltr",
    }}
  >
    <Icon name="remove" size={18} />
    <Text weight={600}>1</Text>
    <Icon name="add" size={18} />
  </div>
);
const Section: React.FC<{ children: React.ReactNode; all?: boolean }> = ({
  children,
  all = false,
}) => (
  <Row>
    <Row style={{ justifyContent: "flex-start" }}>
      <div
        style={{
          width: 6,
          height: 24,
          borderRadius: 99,
          background: P.primary,
        }}
      />
      <Text size={20} weight={600}>
        {children}
      </Text>
    </Row>
    {all && (
      <Text size={14} color={P.primary}>
        عرض الكل
      </Text>
    )}
  </Row>
);
const Product: React.FC<{
  file: string;
  name: string;
  category: string;
  price: string;
}> = ({ file, name, category, price }) => (
  <Card
    style={{
      padding: 8,
      border: 0,
      height: 252,
      display: "flex",
      flexDirection: "column",
    }}
  >
    <div style={{ height: 142, flexShrink: 0 }}>
      <Pic file={file} />
    </div>
    <Gap n={7} />
    <Text size={12} weight={700}>
      {category}
    </Text>
    <Text size={16}>{name}</Text>
    <Gap n={8} />
    <Text size={20} weight={700} color={P.primary}>
      {price} ل.س
    </Text>
  </Card>
);
const Home: React.FC = () => (
  <>
    <Header home />
    <div
      style={{
        background: P.border,
        borderRadius: 16,
        height: 54,
        display: "flex",
        alignItems: "center",
        gap: 12,
        padding: "0 16px",
      }}
    >
      <Icon name="search" size={25} />
      <Text color={P.grey}>ابحث في Primo...</Text>
    </div>
    <Gap n={41} />
    <Section all>الأقسام</Section>
    <Gap />
    <Row>
      {[
        ["vegetables.png", "خضار"],
        ["canns.png", "معلبات"],
        ["beverages.png", "مشروبات"],
        ["snacks.png", "سناكات"],
      ].map(([file, name]) => (
        <div key={file} style={{ width: 73, textAlign: "center" }}>
          <div
            style={{
              width: 73,
              height: 73,
              borderRadius: "50%",
              overflow: "hidden",
              background: "#fff",
            }}
          >
            <Pic file={file} cover />
          </div>
          <Text size={12} weight={700}>
            {name}
          </Text>
        </div>
      ))}
    </Row>
    <Gap n={32} />
    <Section all>أحدث المنتجات</Section>
    <Gap />
    <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
      <Product file="tomato.png" name="بندورة" category="خضار" price="10,000" />
      <Product
        file="oil.jpg"
        name="زيت نباتي"
        category="مواد غذائية"
        price="25,000"
      />
    </div>
    <Nav />
  </>
);
const Details: React.FC = () => (
  <>
    <Header favorite />
    <div style={{ height: 250, borderRadius: 16, overflow: "hidden" }}>
      <Pic file="tomato.png" cover />
    </div>
    <Gap />
    <Row>
      <Text size={32} weight={700}>
        بندورة
      </Text>
      <Text size={24} weight={700} color={P.primary}>
        10,000 ل.س
      </Text>
    </Row>
    <Gap n={8} />
    <Row style={{ justifyContent: "flex-start" }}>
      <Icon name="star_rate" size={24} />
      <Text size={14}>5.0 (0 تقييم)</Text>
    </Row>
    <Gap />
    <Card style={{ padding: 14, borderColor: "#BB001359", borderRadius: 14 }}>
      <Row style={{ justifyContent: "flex-start" }}>
        <Icon name="edit_note_rounded" size={22} />
        <Text size={14} weight={700}>
          ملاحظة اختيارية (اكتب الطعم أو أي تفاصيل)
        </Text>
      </Row>
      <Gap n={12} />
      <div
        style={{
          padding: 12,
          border: `1px solid ${P.border}`,
          borderRadius: 12,
        }}
      >
        <Text size={14} color={P.grey}>
          أضف ملاحظة (مثل الطعم المطلوب)...
        </Text>
      </div>
    </Card>
    <Gap />
    <Card
      style={{
        background: "#F3F3F4",
        border: 0,
        padding: 12,
        borderRadius: 12,
      }}
    >
      <Row>
        <Row>
          <Icon name="qr_code_2_rounded" size={20} color={P.brown} />
          <Text size={14}>SKU: DEMO</Text>
        </Row>
        <Text size={14} color="#2E7D32">
          ● متوفر (10)
        </Text>
      </Row>
    </Card>
    <Gap />
    <Text size={18} weight={700}>
      الوصف
    </Text>
    <Text size={14} color={P.grey}>
      خضار طازجة للطبخ اليومي.
    </Text>
    <div
      style={{
        position: "absolute",
        left: 24,
        right: 24,
        bottom: 24,
        background: P.bg,
      }}
    >
      <Row style={{ justifyContent: "flex-end", marginBottom: 16 }}>
        <Counter />
      </Row>
      <Button>أضف إلى السلة</Button>
    </div>
  </>
);
const Cart: React.FC = () => (
  <>
    <Header />
    <Gap n={20} />
    <Row>
      <Text size={20} weight={600}>
        عربة التسوق
      </Text>
      <div
        style={{ background: P.border, borderRadius: 999, padding: "4px 12px" }}
      >
        <Text size={14}>2 عناصر</Text>
      </div>
    </Row>
    <Gap />
    {[
      ["tomato.png", "بندورة", "10,000"],
      ["oil.jpg", "زيت نباتي", "25,000"],
    ].map(([file, name, price]) => (
      <Card
        key={file}
        style={{ marginBottom: 16, padding: 12, borderRadius: 12 }}
      >
        <Row style={{ alignItems: "flex-start" }}>
          <div style={{ width: 80, height: 100 }}>
            <Pic file={file} />
          </div>
          <div style={{ flex: 1 }}>
            <Text size={16} weight={600}>
              {name}
            </Text>
            <Text size={12} color={P.grey}>
              {file === "tomato.png" ? "1 كغ" : "1 لتر"}
            </Text>
            <Gap n={8} />
            <Text size={18} weight={700} color={P.primary}>
              {price} ل.س
            </Text>
          </div>
          <Icon name="delete_outline" color={P.primary} size={22} />
        </Row>
        <Gap n={12} />
        <Row>
          <Counter />
          <Icon name="edit_note_rounded" size={22} color={P.grey} />
        </Row>
      </Card>
    ))}
    <Gap n={8} />
    <Card style={{ borderRadius: 12 }}>
      <Row>
        <Text size={18} weight={600}>
          الإجمالي:
        </Text>
        <Text size={20} weight={700} color={P.primary}>
          35,000 ل.س
        </Text>
      </Row>
    </Card>
    <Gap n={24} />
    <Button arrow>متابعة للدفع</Button>
    <Nav active="cart" />
  </>
);
const Summary: React.FC = () => (
  <Card>
    <Row>
      <Text>المجموع الفرعي</Text>
      <Text>35,000.00 ل.س</Text>
    </Row>
    <Gap n={12} />
    <Row>
      <Text>رسوم التوصيل</Text>
      <Text>5,000.00 ل.س</Text>
    </Row>
    <Gap />
    <div style={{ height: 1, background: P.border }} />
    <Gap />
    <Row>
      <Text size={18} weight={700}>
        الإجمالي
      </Text>
      <Text size={20} weight={700} color={P.primary}>
        40,000.00 ل.س
      </Text>
    </Row>
  </Card>
);
const Checkout: React.FC = () => (
  <>
    <Header title="إتمام الطلب" plain />
    <Gap n={20} />
    <Text size={18} weight={700}>
      طريقة الاستلام
    </Text>
    <Gap />
    <Row>
      {[
        {
          label: "توصيل للعنوان",
          sub: "يصلك في أقرب وقت",
          icon: "local_shipping",
          selected: true,
        },
        {
          label: "استلام من المتجر",
          sub: "جاهز للاستلام المباشر",
          icon: "storefront_outlined",
          selected: false,
        },
      ].map((v) => (
        <Card
          key={v.label}
          style={{
            flex: 1,
            borderColor: v.selected ? P.primary : P.border,
            borderWidth: v.selected ? 1.5 : 1,
            padding: "16px 10px",
            textAlign: "center",
          }}
        >
          <Row style={{ justifyContent: "center" }}>
            <Icon
              name={v.selected ? "check_circle" : "radio_button_unchecked"}
              size={20}
              color={v.selected ? P.primary : "#CCC5C3"}
            />
            <Icon
              name={v.icon as IconName}
              size={28}
              color={v.selected ? P.primary : P.brown}
            />
          </Row>
          <Gap n={12} />
          <Text size={16} weight={700}>
            {v.label}
          </Text>
          <Text size={12} color={P.grey}>
            {v.sub}
          </Text>
        </Card>
      ))}
    </Row>
    <Gap n={32} />
    <Row>
      <Text size={18} weight={700}>
        عنوان التوصيل
      </Text>
      <Text size={14} weight={700} color={P.primary}>
        تغيير
      </Text>
    </Row>
    <Gap />
    <Card style={{ borderColor: "#E2E2E24D" }}>
      <Row>
        <div>
          <Text size={16} weight={700}>
            البيت — بيانات تجريبية
          </Text>
          <Text size={14} color={P.grey}>
            عنوان توضيحي، لا يخص أي عميل
          </Text>
        </div>
        <div style={{ background: "#F3F3F4", borderRadius: "50%", padding: 8 }}>
          <Icon name="location_on" size={24} color="#625D5C" />
        </div>
      </Row>
    </Card>
    <Gap n={32} />
    <Text size={18} weight={700}>
      ملخص الطلب
    </Text>
    <Gap />
    <Summary />
    <div style={{ position: "absolute", left: 24, right: 24, bottom: 24 }}>
      <Button>تأكيد الطلب</Button>
    </div>
  </>
);
const Confirmed: React.FC = () => (
  <>
    <Header />
    <Gap n={20} />
    <Row>
      <Text size={20} weight={700}>
        طلباتي
      </Text>
      <Icon name="filter_list_rounded" />
    </Row>
    <Gap n={24} />
    <Card>
      <Row style={{ alignItems: "flex-start" }}>
        <div style={{ background: P.bg, borderRadius: "50%", padding: 10 }}>
          <Icon name="shopping_bag_outlined" size={20} />
        </div>
        <div style={{ flex: 1 }}>
          <Text size={20} weight={600}>
            طلب #DEMO
          </Text>
          <Text size={12} color={P.grey}>
            الآن
          </Text>
        </div>
        <Text size={20} weight={700} color={P.primary}>
          40,000 ل.س
        </Text>
      </Row>
      <Gap />
      <Row style={{ justifyContent: "flex-start" }}>
        <div
          style={{
            borderRadius: 999,
            background: "#F3F3F4",
            padding: "4px 10px",
          }}
        >
          <Row>
            <Icon name="local_shipping" size={14} color="#5A5C5D" />
            <Text size={12}>توصيل</Text>
          </Row>
        </div>
        <div
          style={{
            borderRadius: 999,
            background: "#FFF3E0",
            padding: "4px 10px",
          }}
        >
          <Row>
            <Icon name="schedule_rounded" size={14} color="#E65100" />
            <Text size={12} weight={700} color="#E65100">
              قيد الانتظار
            </Text>
          </Row>
        </div>
      </Row>
      <Gap />
      <div style={{ height: 1, background: P.border }} />
      <Gap />
      <Row>
        <Row>
          <Pic file="tomato.png" width={32} height={32} />
          <Pic file="oil.jpg" width={32} height={32} />
        </Row>
        <Text size={14} color={P.primary}>
          عرض التفاصيل ←
        </Text>
      </Row>
    </Card>
    <div
      style={{
        position: "absolute",
        bottom: 84,
        left: -8,
        right: -8,
        background: "#2E7D32",
        borderRadius: 12,
        padding: "14px 16px",
        color: "#fff",
        display: "flex",
        alignItems: "center",
        gap: 10,
      }}
    >
      <Text size={14} weight={600} color="#fff">
        تم تأكيد الطلب بنجاح!
      </Text>
    </div>
    <Nav active="orders" />
  </>
);
export const PrimoUI: React.FC = () => {
  const f = useCurrentFrame();
  const start = f < 22 ? 0 : f < 46 ? 22 : f < 70 ? 46 : f < 97 ? 70 : 97;
  return (
    <div
      dir="rtl"
      lang="ar"
      data-ui-origin="source-reconstruction-demo"
      style={{
        position: "relative",
        width: 390,
        height: 884.76,
        background: P.bg,
        color: P.text,
        fontFamily: "Cairo",
        fontWeight: 400,
        padding: "18px 24px 0",
        overflow: "hidden",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 6,
          left: 16,
          fontFamily: "Space",
          fontSize: 8,
          color: P.grey,
        }}
      >
        DEMO · SOURCE RECONSTRUCTION
      </div>
      <div
        style={{
          position: "relative",
          height: "100%",
          translate: `${ease(f, start, start + 5, 20, 0)}px 0px`,
          opacity: ease(f, start, start + 4, 0.35, 1),
        }}
      >
        {f < 22 ? (
          <Home />
        ) : f < 46 ? (
          <Details />
        ) : f < 70 ? (
          <Cart />
        ) : f < 97 ? (
          <Checkout />
        ) : (
          <Confirmed />
        )}
      </div>
      {((f >= 35 && f < 43) || (f >= 87 && f < 96)) && (
        <div
          style={{
            position: "absolute",
            left: 120,
            top: f < 46 ? 800 : 801,
            width: 90,
            height: 90,
            border: "3px solid #BB0013",
            background: "#BB001320",
            borderRadius: "50%",
            scale: ease(f, f < 46 ? 35 : 87, f < 46 ? 43 : 96, 0.3, 1.5),
            opacity: ease(f, f < 46 ? 35 : 87, f < 46 ? 43 : 96, 1, 0),
            pointerEvents: "none",
          }}
        />
      )}
    </div>
  );
};
