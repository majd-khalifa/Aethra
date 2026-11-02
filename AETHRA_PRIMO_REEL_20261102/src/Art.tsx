// REJECTED DESIGN CHECKPOINT: current characters and illustration style are NOT approved.
// Preserved for history only. Await the user's revised creative brief before new art work.
import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
export const C = {
  ink: "#302f39",
  skin: "#e7ab84",
  hair: "#30303b",
  cream: "#fff0d8",
  teal: "#327773",
  red: "#d8674c",
  purple: "#74639e",
};
export const ease = (f: number, a: number, b: number, x: number, y: number) =>
  interpolate(f, [a, b], [x, y], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
export const Svg: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <svg
    width="1080"
    height="1920"
    viewBox="0 0 1080 1920"
    style={{ position: "absolute", inset: 0 }}
  >
    <defs>
      <linearGradient id="wall" x2="0.4" y2="1">
        <stop stopColor="#ffefd4" />
        <stop offset="1" stopColor="#ead5bd" />
      </linearGradient>
      <linearGradient id="door" x2="1" y2="0">
        <stop stopColor="#347f7a" />
        <stop offset="1" stopColor="#225657" />
      </linearGradient>
      <pattern id="tiles" width="90" height="90" patternUnits="userSpaceOnUse">
        <rect width="90" height="90" fill="#ecdfca" />
        <path
          d="M45 8L82 45 45 82 8 45Z"
          fill="none"
          stroke="#81a49b"
          strokeWidth="2"
          opacity=".4"
        />
        <circle cx="45" cy="45" r="6" fill="#81a49b" opacity=".3" />
      </pattern>
    </defs>
    {children}
  </svg>
);
export const Room: React.FC<{ kitchen?: boolean }> = ({ kitchen = false }) => (
  <>
    <rect width="1080" height="1920" fill="url(#wall)" />
    <path d="M0 1450H1080V1920H0Z" fill="#c99d7e" />
    <path d="M0 1450H1080M0 1470H1080" stroke="#ab8066" strokeWidth="8" />
    {[0, 1, 2, 3, 4, 5].map((i) => (
      <path
        key={i}
        d={`M${i * 240 - 170} 1920L${i * 160 + 60} 1450`}
        stroke="#ad8269"
        strokeWidth="3"
        opacity=".4"
      />
    ))}
    <rect
      x="70"
      y="240"
      width="360"
      height="480"
      rx="180"
      fill="#537e7c"
      stroke="#c2a183"
      strokeWidth="20"
    />
    <path d="M90 540Q250 440 410 550V700H90" fill="#789f92" />
    <path d="M250 258V700M85 475H415" stroke="#eadac4" strokeWidth="12" />
    <path
      d="M70 250Q135 415 60 735M430 250Q370 415 440 735"
      fill="#e4a17e"
      stroke="#bc7c63"
      strokeWidth="6"
    />
    <circle
      cx="840"
      cy="360"
      r="88"
      fill="#fff4dc"
      stroke="#b58f70"
      strokeWidth="12"
    />
    <path
      d="M840 300V360L877 382"
      fill="none"
      stroke={C.ink}
      strokeWidth="10"
      strokeLinecap="round"
    />
    {kitchen ? (
      <>
        <rect x="0" y="745" width="1080" height="445" fill="url(#tiles)" />
        <rect x="0" y="1125" width="1080" height="370" fill="#518c83" />
        {[30, 300, 570, 840].map((x) => (
          <g key={x}>
            <rect
              x={x}
              y="1180"
              width="230"
              height="260"
              rx="7"
              fill="#6a9b8e"
              stroke="#376a64"
              strokeWidth="4"
            />
            <path
              d={`M${x + 85} 1225h55`}
              stroke="#e7c69f"
              strokeWidth="8"
              strokeLinecap="round"
            />
          </g>
        ))}
        <rect x="0" y="1105" width="1080" height="35" rx="15" fill="#f8e5cb" />
        <path d="M550 1090h330" stroke="#3b3b3c" strokeWidth="20" />
        <path
          d="M625 990H810L790 1090H645Z"
          fill="#bfc2b5"
          stroke="#6b7770"
          strokeWidth="6"
        />
        <path
          d="M610 1005h-25m240 0h25"
          stroke="#6b7770"
          strokeWidth="15"
          strokeLinecap="round"
        />
        <ellipse cx="718" cy="988" rx="93" ry="12" fill="#6c7b6e" />
      </>
    ) : (
      <>
        <rect x="485" y="820" width="540" height="435" rx="75" fill="#c77c66" />
        <rect
          x="460"
          y="1070"
          width="590"
          height="250"
          rx="60"
          fill="#b86b58"
        />
        <rect
          x="505"
          y="1045"
          width="230"
          height="130"
          rx="40"
          fill="#de9980"
        />
        <rect
          x="750"
          y="1045"
          width="230"
          height="130"
          rx="40"
          fill="#de9980"
        />
        <path d="M510 1315v90m480-90v90" stroke="#825a4e" strokeWidth="25" />
        <ellipse cx="545" cy="1580" rx="475" ry="125" fill="#e4c69e" />
        <ellipse
          cx="545"
          cy="1580"
          rx="410"
          ry="88"
          fill="none"
          stroke="#b88571"
          strokeWidth="6"
        />
      </>
    )}
    <Plant x={100} y={1350} />
  </>
);
const Plant: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <g transform={`translate(${x} ${y})`}>
    <path
      d="M0 0Q-100-230-10-260Q50-150 0 0M0 0Q130-230 145-160Q160-90 0 0M0 0Q-160-130-125-180Q-55-175 0 0"
      fill="#376c5c"
    />
    <path d="M-65 0H70L50 145H-45Z" fill="#bd6f51" />
    <path d="M-70 0H75" stroke="#e7a278" strokeWidth="20" />
  </g>
);
type PersonProps = {
  kind: "mother" | "daughter" | "older" | "younger" | "courier";
  x: number;
  y: number;
  scale?: number;
  pose?:
    | "talk"
    | "annoyed"
    | "roll"
    | "sigh"
    | "phone"
    | "game"
    | "kick"
    | "happy"
    | "surprise";
  flip?: boolean;
};
export const Person: React.FC<PersonProps> = ({
  kind,
  x,
  y,
  scale = 1,
  pose = "happy",
  flip = false,
}) => {
  const f = useCurrentFrame();
  const mom = kind === "mother",
    girl = kind === "daughter",
    young = kind === "younger",
    courier = kind === "courier";
  const female = mom || girl;
  const shirt = mom
    ? C.teal
    : girl
      ? C.purple
      : young
        ? "#e9b64f"
        : courier
          ? C.red
          : "#547b9d";
  const angry = pose === "annoyed" || pose === "talk";
  const eyeRoll = pose === "roll";
  const happy = pose === "happy";
  const blinking = f % 101 > 96;
  const bounce =
    pose === "kick"
      ? Math.sin(f * 0.24) * 7
      : pose === "game"
        ? Math.sin(f * 0.5) * 2
        : Math.sin(f * 0.08) * 2;
  const mouth =
    pose === "talk"
      ? 8 + Math.abs(Math.sin(f * 0.5)) * 10
      : pose === "surprise"
        ? 16
        : pose === "sigh"
          ? 8
          : 0;
  return (
    <g
      transform={`translate(${x} ${y + bounce}) scale(${scale * (flip ? -1 : 1)} ${scale})`}
      stroke={C.ink}
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <ellipse
        cx="0"
        cy="360"
        rx="135"
        ry="22"
        fill="#302f39"
        opacity=".12"
        stroke="none"
      />
      <path
        d={
          pose === "kick"
            ? "M-45 225L-80 330M45 225L145 285"
            : "M-45 225L-49 340M45 225L53 340"
        }
        stroke="#344554"
        strokeWidth="48"
      />
      <path
        d={
          pose === "kick"
            ? "M-102 345h65M125 296l64 13"
            : "M-75 352h65M30 352h70"
        }
        stroke="#f7e5cb"
        strokeWidth="25"
      />
      <path
        d="M-60 58Q-115 75-105 205L-82 250Q0 270 85 250L105 205Q112 80 60 58Z"
        fill={shirt}
        strokeWidth="5"
      />
      {mom && (
        <>
          <path
            d="M-38 65L-65 132V245H70V130L42 65"
            fill="#ead4b3"
            strokeWidth="4"
          />
          <path d="M-35 175h70v40h-70Z" fill="#d4b38e" stroke="none" />
        </>
      )}
      {girl && (
        <>
          <path
            d="M-65 130L-70 215M65 130L70 215"
            fill="none"
            stroke="#594f7a"
            strokeWidth="4"
          />
          <text
            x="0"
            y="170"
            textAnchor="middle"
            fontFamily="Space"
            fontSize="18"
            fill="#f9e7cc"
            stroke="none"
          >
            AETHRA
          </text>
        </>
      )}
      {courier && <path d="M-70 100H70" stroke="#fff0d8" strokeWidth="7" />}
      <path d="M-18 42v35q18 25 38 0V40" fill={C.skin} strokeWidth="4" />
      {female && (
        <path
          d="M-74-70Q-105 20-65 95L-42 42H55L76 92Q106 2 65-72Z"
          fill={C.hair}
          strokeWidth="5"
        />
      )}
      <ellipse cx="-73" cy="-5" rx="14" ry="20" fill={C.skin} strokeWidth="4" />
      <ellipse cx="73" cy="-5" rx="14" ry="20" fill={C.skin} strokeWidth="4" />
      <path
        d="M-70-52Q-68-105 0-108Q72-101 72-52V7Q67 67 0 70Q-64 60-70 7Z"
        fill={C.skin}
        strokeWidth="5"
      />
      <path
        d={
          mom
            ? "M-76-31Q-85-99-20-112Q56-135 80-50L67-10Q35-38 18-78Q-10-20-68-18Z"
            : girl
              ? "M-76-20Q-83-108-8-116Q63-120 79-46L70-2Q33-14 10-76Q-32-16-76-20Z"
              : "M-74-25L-78-71-58-73-65-107-28-91-12-125 10-99 44-111 74-74 77-23 57-39Q12-26-15-57Q-38-22-74-25Z"
        }
        fill={C.hair}
        strokeWidth="4"
      />
      {mom && (
        <circle cx="-48" cy="-103" r="32" fill={C.hair} strokeWidth="4" />
      )}
      {courier && (
        <path
          d="M-76-62Q0-150 77-62H100V-43H-80Z"
          fill={C.red}
          strokeWidth="4"
        />
      )}
      <g transform={`translate(0 ${eyeRoll ? -6 : 0})`}>
        {[-31, 31].map((e, i) => (
          <g key={e}>
            {blinking ? (
              <path d={`M${e - 14}-4q14 8 28 0`} fill="none" strokeWidth="5" />
            ) : (
              <>
                <ellipse
                  cx={e}
                  cy="-5"
                  rx="17"
                  ry={eyeRoll ? 14 : 19}
                  fill="#fff5df"
                  strokeWidth="3"
                />
                <ellipse
                  cx={e + (pose === "phone" ? 5 : eyeRoll ? interpolate(f,[0,5,10,14],[0,-6,1,6],{extrapolateRight:'clamp'}) : 0)}
                  cy={eyeRoll ? interpolate(f,[0,5,10,14],[-3,-10,-14,-10],{extrapolateRight:'clamp'}) : pose === "phone" ? 1 : -3}
                  rx="6"
                  ry="9"
                  fill={C.ink}
                  stroke="none"
                />
                <circle
                  cx={e + (eyeRoll ? interpolate(f,[0,5,10,14],[2,-4,3,8],{extrapolateRight:'clamp'}) : 2)}
                  cy={eyeRoll ? interpolate(f,[0,5,10,14],[-7,-14,-18,-14],{extrapolateRight:'clamp'}) : -7}
                  r="2"
                  fill="white"
                  stroke="none"
                />
              </>
            )}
            <path
              d={
                angry
                  ? `M${e - 16} ${i === 0 ? -31 : -23}l32 ${i === 0 ? 8 : -8}`
                  : `M${e - 15}-30q15 ${pose === "surprise" ? -14 : -6} 30 0`
              }
              fill="none"
              strokeWidth="6"
            />
          </g>
        ))}
      </g>
      <path d="M1-6L-7 15H6" fill="none" stroke="#b57359" strokeWidth="3" />
      {mouth ? (
        <ellipse
          cx="5"
          cy="38"
          rx={mouth * 0.7}
          ry={mouth}
          fill="#75453e"
          strokeWidth="3"
        />
      ) : (
        <path
          d={
            happy
              ? "M-20 33Q0 57 23 31"
              : eyeRoll
                ? "M-12 41q17-9 32-2"
                : "M-16 39q17-7 33 0"
          }
          fill={happy ? "#fff2dd" : "none"}
          strokeWidth="4"
        />
      )}
      <ellipse
        cx="-48"
        cy="22"
        rx="14"
        ry="7"
        fill="#d68670"
        opacity=".6"
        stroke="none"
      />
      <ellipse
        cx="48"
        cy="22"
        rx="14"
        ry="7"
        fill="#d68670"
        opacity=".6"
        stroke="none"
      />
      {female && (
        <>
          <circle cx="-76" cy="19" r="7" fill="#e8b75c" strokeWidth="2" />
          <circle cx="76" cy="19" r="7" fill="#e8b75c" strokeWidth="2" />
        </>
      )}
      {pose === "phone" ? (
        <>
          <path
            d="M-94 110L-56 196 52 164M91 110L64 154"
            fill="none"
            stroke={C.skin}
            strokeWidth="29"
          />
          <g transform="translate(50 138) rotate(12)">
            <rect
              x="-27"
              y="-47"
              width="60"
              height="104"
              rx="10"
              fill={C.ink}
              strokeWidth="4"
            />
            <rect
              x="-19"
              y="-32"
              width="44"
              height="72"
              rx="3"
              fill="#eae7df"
              stroke="none"
            />
          </g>
          <circle cx="71" cy="173" r="15" fill={C.skin} strokeWidth="3" />
        </>
      ) : pose === "game" ? (
        <>
          <path
            d="M-95 110L-70 190-20 164M95 110L70 190 20 164"
            fill="none"
            stroke={C.skin}
            strokeWidth="28"
          />
          <path
            d="M-45 148Q0 133 45 148L60 183Q52 209 30 180H-30Q-56 210-60 183Z"
            fill="#444454"
            strokeWidth="4"
          />
          <path d="M-34 153v22m-11-11h22" stroke="#eadccd" strokeWidth="4" />
          <circle cx="30" cy="157" r="5" fill="#dc7058" stroke="none" />
          <circle cx="40" cy="168" r="5" fill="#86b29d" stroke="none" />
          <path
            d="M-86-36Q-111-120 0-129Q111-120 86-36"
            fill="none"
            stroke="#d57958"
            strokeWidth="15"
          />
          <rect
            x="-97"
            y="-48"
            width="24"
            height="56"
            rx="10"
            fill="#d57958"
            strokeWidth="3"
          />
          <rect
            x="73"
            y="-48"
            width="24"
            height="56"
            rx="10"
            fill="#d57958"
            strokeWidth="3"
          />
        </>
      ) : (
        <>
          <path
            d={
              angry
                ? `M-95 105L-143 ${110 + Math.sin(f * 0.2) * 12}-164 16`
                : "M-95 105L-118 190-85 210"
            }
            fill="none"
            stroke={C.skin}
            strokeWidth="29"
          />
          <path
            d={happy ? "M95 105L134 148 172 91" : "M95 105L120 185 81 211"}
            fill="none"
            stroke={C.skin}
            strokeWidth="29"
          />
          {angry && (
            <g transform="rotate(-12 -164 30)">
              <path d="M-164 40V-38" stroke="#ba8863" strokeWidth="12" />
              <ellipse
                cx="-164"
                cy="-61"
                rx="19"
                ry="30"
                fill="#ba8863"
                strokeWidth="3"
              />
            </g>
          )}
        </>
      )}
    </g>
  );
};
export const Ball: React.FC<{ x: number; y: number; angle?: number }> = ({
  x,
  y,
  angle = 0,
}) => (
  <g transform={`translate(${x} ${y}) rotate(${angle})`}>
    <circle r="48" fill="#fff0d8" stroke={C.ink} strokeWidth="5" />
    <path d="M0-21L22-7 15 20H-15L-22-7Z" fill={C.ink} />
    <path
      d="M0-21V-47M22-7L44-15M15 20L30 38M-15 20L-30 38M-22-7L-44-15"
      stroke={C.ink}
      strokeWidth="5"
    />
  </g>
);
export const Groceries: React.FC<{ x: number; y: number; scale?: number }> = ({
  x,
  y,
  scale = 1,
}) => (
  <g
    transform={`translate(${x} ${y}) scale(${scale})`}
    stroke={C.ink}
    strokeWidth="4"
    strokeLinejoin="round"
  >
    <path d="M-70 0l-18-120 26-13 25 130" fill="#ecba68" />
    <path d="M-70-99l22 14m-18 8l22 14" stroke="#bf8e4e" />
    <path
      d="M30 10Q12-65 38-110Q88-113 61-43Q105-92 119-69Q115-30 70 15"
      fill="#508459"
    />
    <circle cx="-5" cy="-16" r="39" fill="#de6850" />
    <path d="M-26-49L-7-38 13-50 5-28" fill="#44724c" />
    <path d="M-95-5H100L80 165H-75Z" fill="#c79765" />
    <path
      d="M-37 25V-10Q0-65 40-10V25"
      fill="none"
      stroke="#805d43"
      strokeWidth="9"
    />
    <path d="M-65 120H68" stroke="#dfb580" />
  </g>
);
