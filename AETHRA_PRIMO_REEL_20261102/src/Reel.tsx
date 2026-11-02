// STOPPED BY USER: this draft's character designs and illustration style are REJECTED.
// See ../../PRODUCTION_HANDOFF.md. Do not render or redesign until explicitly resumed.
import React from "react";
import {
  AbsoluteFill,
  Sequence,
  Audio,
  Img,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  Easing,
} from "remotion";
import { C, Svg, Room, Person, Ball, Groceries, ease } from "./Art";
import captions from "./captions.json";
import "./style.css";
import { PrimoUI } from "./PrimoUI";

const Arabic: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
}> = ({ children, style }) => (
  <div dir="rtl" lang="ar-SY" className="arabic" style={style}>
    {children}
  </div>
);
const Subtitles: React.FC = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const c = captions.find(
    (c) => (f * 1000) / fps >= c.startMs && (f * 1000) / fps < c.endMs,
  );
  return c ? (
    <div
      style={{
        position: "absolute",
        bottom: 235,
        left: 80,
        right: 80,
        textAlign: "center",
      }}
    >
      <Arabic
        style={{
          fontSize: 51,
          lineHeight: 1.65,
          color: C.cream,
          background: C.ink,
          borderRadius: 25,
          padding: "18px 25px",
          boxShadow: "0 10px 0 #302f3920",
        }}
      >
        {c.text}
      </Arabic>
    </div>
  ) : null;
};
const Steam: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <g
      fill="none"
      stroke="#fff9ee"
      strokeWidth="13"
      strokeLinecap="round"
      opacity=".7"
    >
      {[0, 1, 2].map((i) => (
        <path
          key={i}
          d={`M${670 + i * 46} ${930 - ((f + i * 10) % 36)}q-30-35 0-65t0-60`}
        />
      ))}
    </g>
  );
};
const Kitchen: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill>
      <Svg>
        <g
          transform={`translate(${-ease(f, 0, 60, 0, 12)} 0) scale(${ease(f, 0, 60, 1, 1.025)})`}
        >
          <Room kitchen />
          <Steam />
          <Person
            kind="mother"
            x={350}
            y={870}
            scale={1.75}
            pose={f < 150 ? "talk" : "annoyed"}
          />
          <rect
            x="480"
            y="1090"
            width="100"
            height="22"
            rx="6"
            fill="#c99870"
          />
          <path
            d="M500 1078l28-15m-10 14l35-20"
            stroke="#729759"
            strokeWidth="10"
            strokeLinecap="round"
          />
        </g>
        {f >= 150 && (
          <g
            transform={`translate(850 780) scale(${ease(f, 150, 158, 0.4, 1)})`}
            fill={C.red}
          >
            <path d="M-15-80H15L10 10H-10Z" />
            <circle cy="35" r="15" />
          </g>
        )}
      </Svg>
      <Subtitles />
    </AbsoluteFill>
  );
};
const Boys: React.FC = () => {
  const f = useCurrentFrame();
  const foot = f >= 45;
  return (
    <AbsoluteFill>
      <Svg>
        <Room />
        {foot ? (
          <>
            <Person kind="younger" x={510} y={830} scale={1.6} pose="kick" />
            <Ball
              x={720 + Math.sin(f * 0.17) * 180}
              y={1350 - Math.abs(Math.sin(f * 0.17)) * 150}
              angle={f * 9}
            />
            <path
              d="M150 1370l120-65m-90 120l90-30"
              stroke="#fff0d8"
              strokeWidth="10"
              strokeLinecap="round"
            />
          </>
        ) : (
          <>
            <rect
              x="90"
              y="740"
              width="240"
              height="220"
              rx="18"
              fill="#363a46"
            />
            <rect
              x="110"
              y="758"
              width="200"
              height="170"
              rx="8"
              fill="#8ca99b"
            />
            <path
              d={`M130 ${850 + Math.sin(f * 0.2) * 35}l65-35 90 65`}
              stroke="#ead793"
              strokeWidth="10"
              fill="none"
            />
            <path
              d="M210 960v120m-70 0h140"
              stroke="#363a46"
              strokeWidth="15"
            />
            <Person kind="older" x={700} y={850} scale={1.6} pose="game" />
            <path
              d="M900 590l30-65m-3 100l63-30"
              fill="none"
              stroke="#bf7b62"
              strokeWidth="10"
              strokeLinecap="round"
            />
          </>
        )}
        <g transform="translate(150 400)">
          <path
            d="M0 0Q-35-65 30-75Q80-80 72-22Q63 3 35 13"
            stroke={C.red}
            strokeWidth="12"
            fill="none"
          />
          <circle cx="32" cy="45" r="7" fill={C.red} />
        </g>
      </Svg>
      <Arabic
        style={{
          position: "absolute",
          top: 200,
          right: 90,
          color: C.ink,
          fontSize: 44,
        }}
      >
        {foot ? "والصغير… بالمباراة" : "الكبير… بالمهمة"}
      </Arabic>
    </AbsoluteFill>
  );
};
const Daughter: React.FC = () => {
  const f = useCurrentFrame();
  const walk = ease(f, 28, 51, 0, 390);
  const close = interpolate(f, [44, 56], [0.28, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.bezier(0.45, 0, 0.8, 1),
  });
  return (
    <AbsoluteFill>
      <Svg>
        <Room />
        <rect
          x="540"
          y="500"
          width="400"
          height="970"
          rx="10"
          fill="#18383e"
          stroke="#d4b08b"
          strokeWidth="25"
        />
        <path d="M555 1450L925 1400V535H555" fill="#5c5571" />
        <rect x="680" y="710" width="180" height="320" rx="15" fill="#8d7cad" />
        <path d="M600 1120H920V1420H600Z" fill="#7f6d94" />
        {f < 53 && (
          <Person
            kind="daughter"
            x={300 + walk}
            y={f < 28 ? 860 : 860 - Math.abs(Math.sin(f * 0.55)) * 10}
            scale={1.7}
            pose={f < 15 ? "roll" : f < 29 ? "sigh" : "phone"}
          />
        )}
        <g transform={`translate(935 515) scale(${close} 1)`}>
          <rect
            x="-385"
            width="385"
            height="940"
            rx="5"
            fill="url(#door)"
            stroke="#255354"
            strokeWidth="10"
          />
          <rect
            x="-350"
            y="190"
            width="310"
            height="245"
            rx="5"
            fill="none"
            stroke="#4b8c82"
            strokeWidth="9"
          />
          <rect
            x="-350"
            y="475"
            width="310"
            height="405"
            rx="5"
            fill="none"
            stroke="#4b8c82"
            strokeWidth="9"
          />
          <circle cx="-325" cy="470" r="16" fill="#e6b76b" />
        </g>
        <g
          transform={
            f < 57
              ? `translate(${935 - 245 * close} 770) scale(${close} 1) rotate(-5)`
              : `translate(${690 + ease(f, 58, 75, 0, -45)} ${770 + ease(f, 58, 75, 0, 640)}) rotate(${ease(f, 57, 75, -5, 95)})`
          }
          opacity={ease(f, 70, 75, 1, 0)}
        >
          <rect
            x="-100"
            y="-48"
            width="245"
            height="85"
            rx="8"
            fill="#fff1d6"
            stroke="#d8c3a6"
            strokeWidth="3"
          />
          <text
            x="20"
            y="7"
            textAnchor="middle"
            fontFamily="Space"
            fontSize="31"
            fill={C.ink}
          >
            AETHRA LAB
          </text>
          {f > 56 && <path d="M145-48L105-48 145-5Z" fill="#bba88d" />}
        </g>
        {f > 15 && f < 29 && (
          <g
            opacity={Math.sin(((f - 15) / 14) * Math.PI)}
            stroke="#fff5e1"
            strokeWidth="9"
            fill="none"
            strokeLinecap="round"
          >
            <path d="M390 915q70 10 100-30M395 935q70 25 100 5" />
          </g>
        )}
      </Svg>
    </AbsoluteFill>
  );
};

// Authorized source-verified reconstruction. No authenticated captures or live orders.
export const AppScene: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#e6dced" }}>
      <Svg>
        <rect width="1080" height="1920" fill="#e6dced" />
        <circle cx="950" cy="520" r="500" fill="#d1c2df" />
        <circle cx="60" cy="1500" r="460" fill="#c0afa3" />
        <Person kind="daughter" x={205} y={1170} scale={1.2} pose="phone" />
        <path
          d="M80 1600H1000"
          stroke="#aa907b"
          strokeWidth="20"
          strokeLinecap="round"
        />
      </Svg>
      <div
        style={{
          position: "absolute",
          left: 360,
          top: 245,
          width: 650,
          height: 1440,
          border: "14px solid #302f39",
          borderRadius: 47,
          overflow: "hidden",
          boxShadow: "20px 30px 0 #302f3922",
          rotate: `${ease(f, 0, 18, 5, 0)}deg`,
          scale: ease(f, 0, 16, 0.85, 1),
          background: "#fff",
        }}
      >
        <div
          style={{
            scale: 622 / 390,
            transformOrigin: "top left",
            width: 390,
            height: 884.76,
          }}
        >
          <PrimoUI />
        </div>
      </div>
      <Arabic
        style={{
          position: "absolute",
          top: 130,
          left: 90,
          right: 90,
          fontSize: 52,
          color: C.ink,
          textAlign: "center",
        }}
      >
        الحل بإيدها.
      </Arabic>
      <Arabic
        style={{
          position: "absolute",
          bottom: 135,
          left: 90,
          right: 90,
          fontSize: 29,
          color: C.ink,
          textAlign: "center",
        }}
      >
        محاكاة من كود التطبيق • بيانات للتجربة
      </Arabic>
    </AbsoluteFill>
  );
};
const TimeJump: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill
      style={{
        background: C.teal,
        alignItems: "center",
        justifyContent: "center",
      }}
    >
      <Svg>
        <circle cx="540" cy="800" r="195" fill={C.cream} />
        <circle
          cx="540"
          cy="800"
          r="170"
          fill="none"
          stroke="#b0c1aa"
          strokeWidth="5"
        />
        <path
          d="M540 800V675"
          stroke={C.ink}
          strokeWidth="15"
          strokeLinecap="round"
          transform={`rotate(${f * 28} 540 800)`}
        />
        <path
          d="M540 800l80 30"
          stroke={C.ink}
          strokeWidth="15"
          strokeLinecap="round"
        />
        <circle cx="540" cy="800" r="15" fill={C.red} />
        {[0, 1, 2].map((i) => (
          <path
            key={i}
            d={`M${150 + i * 20} ${660 + i * 130}h100`}
            stroke="#8caaa0"
            strokeWidth="10"
            strokeLinecap="round"
          />
        ))}
      </Svg>
      <Arabic
        style={{
          position: "absolute",
          top: 1100,
          fontSize: 70,
          color: C.cream,
        }}
      >
        بعد شوي…
      </Arabic>
    </AbsoluteFill>
  );
};
const Arrival: React.FC = () => {
  const f = useCurrentFrame();
  const peace = f >= 38;
  return (
    <AbsoluteFill>
      <Svg>
        <Room />
        {!peace ? (
          <>
            <rect
              x="690"
              y="420"
              width="370"
              height="1020"
              fill="#7f9b93"
              stroke="#d5b28d"
              strokeWidth="20"
            />
            <Person
              kind="courier"
              x={835 + ease(f, 0, 15, 100, 0)}
              y={810}
              scale={1.4}
              pose="happy"
            />
            <Person
              kind="mother"
              x={340}
              y={850}
              scale={1.7}
              pose={f < 25 ? "surprise" : "happy"}
            />
            <Groceries x={655} y={1170} scale={1.35} />
            <g
              transform={`translate(615 540) rotate(${Math.sin(f * 0.8) * 13})`}
              stroke={C.red}
              strokeWidth="12"
              fill="none"
              strokeLinecap="round"
            >
              <path d="M-35 0Q-35-70 0-70Q35-70 35 0l15 14h-100Z" />
              <path d="M-9 30q9 9 18 0M-68-32l-12-17M68-32l12-17" />
            </g>
          </>
        ) : (
          <>
            <Person kind="older" x={800} y={865} scale={1.1} pose="happy" />
            <Person kind="younger" x={595} y={1020} scale={0.95} pose="happy" />
            <Person kind="mother" x={270} y={830} scale={1.6} pose="happy" />
            <Person
              kind="daughter"
              x={850}
              y={1220}
              scale={0.95}
              pose="happy"
            />
            <Groceries x={420} y={1240} scale={1.1} />
            <Ball x={580} y={1490} />
            <path
              d="M410 650q15-45 30 0q15-45 30 0q0 20-30 42q-30-22-30-42"
              fill={C.red}
            />
          </>
        )}
      </Svg>
      {peace && (
        <Arabic
          style={{
            position: "absolute",
            top: 190,
            left: 90,
            right: 90,
            textAlign: "center",
            fontSize: 58,
            color: C.ink,
          }}
        >
          وهيك… رِوِق البيت.
        </Arabic>
      )}
    </AbsoluteFill>
  );
};
const End: React.FC = () => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: "#050505", alignItems: "center" }}>
      <Img
        src={staticFile("brand/primo-original.png")}
        style={{
          position: "absolute",
          top: 180,
          width: 700,
          height: 700,
          objectFit: "contain",
          opacity: 1,
          scale: ease(f, 0, 18, 0.92, 1),
        }}
      />
      <Arabic
        style={{
          position: "absolute",
          top: 950,
          fontSize: 94,
          color: "#fff2df",
          lineHeight: 1.4,
          opacity: ease(f, 7, 18, 0, 1),
        }}
      >
        مشوارك علينا!
      </Arabic>
      <Arabic
        style={{
          position: "absolute",
          top: 1155,
          fontSize: 51,
          color: "#f2d9bd",
          opacity: ease(f, 15, 26, 0, 1),
        }}
      >
        اطلبها… وبتوصلك لعندك.
      </Arabic>
      <div
        style={{
          position: "absolute",
          top: 1515,
          display: "flex",
          gap: 22,
          alignItems: "center",
          opacity: ease(f, 20, 30, 0, 1),
        }}
      >
        <span style={{ fontFamily: "Space", fontSize: 22, color: "#b2a6bc" }}>
          PRODUCED BY
        </span>
        <div
          style={{ background: "#fff", borderRadius: 10, padding: "12px 20px" }}
        >
          <Img
            src={staticFile("brand/aethra-approved.png")}
            style={{ width: 190, height: 55, objectFit: "contain" }}
          />
        </div>
      </div>
    </AbsoluteFill>
  );
};
export const PrimoReel: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill style={{ background: C.cream }}>
      <Sequence name="Mother needs groceries" durationInFrames={7 * fps}>
        <Kitchen />
      </Sequence>
      <Sequence
        name="Sons do not answer"
        from={2 * fps}
        durationInFrames={3 * fps}
      >
        <Boys />
        <SubtitlesOffset />
      </Sequence>
      <Sequence
        name="AETHRA eye roll, sigh, door, peeling sticker"
        from={7 * fps}
        durationInFrames={2.5 * fps}
      >
        <Daughter />
      </Sequence>
      <Sequence
        name="Primo UI reconstructed from original source - demo data"
        from={9.5 * fps}
        durationInFrames={4 * fps}
      >
        <AppScene />
      </Sequence>
      <Sequence
        name="Comedic time jump"
        from={13.5 * fps}
        durationInFrames={fps}
      >
        <TimeJump />
      </Sequence>
      <Sequence
        name="Doorbell, groceries, family peace"
        from={14.5 * fps}
        durationInFrames={2.5 * fps}
      >
        <Arrival />
      </Sequence>
      <Sequence
        name="Original Primo logo and AETHRA production credit"
        from={17 * fps}
        durationInFrames={3 * fps}
      >
        <End />
      </Sequence>
      <Audio src={staticFile("audio/final-mix.wav")} />
    </AbsoluteFill>
  );
};
const SubtitlesOffset: React.FC = () => {
  const f = useCurrentFrame() + 60;
  const c = captions.find(
    (c) => (f * 1000) / 30 >= c.startMs && (f * 1000) / 30 < c.endMs,
  );
  return c ? (
    <div
      style={{
        position: "absolute",
        bottom: 235,
        left: 80,
        right: 80,
        textAlign: "center",
      }}
    >
      <Arabic
        style={{
          fontSize: 51,
          lineHeight: 1.65,
          color: C.cream,
          background: C.ink,
          borderRadius: 25,
          padding: "18px 25px",
        }}
      >
        {c.text}
      </Arabic>
    </div>
  ) : null;
};
