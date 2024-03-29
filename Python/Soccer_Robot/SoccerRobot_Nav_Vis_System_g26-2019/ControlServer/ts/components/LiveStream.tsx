import styled, { css } from "styled-components";
import { useEffect, Dispatch, useState, Fragment, SetStateAction } from "react";
import { useApi } from "../api";
import WSAvcPlayer from "ws-avc-player";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import {
  faExpand,
  faPlayCircle,
  faStopCircle
} from "@fortawesome/free-solid-svg-icons";
import { Stage, Layer, Rect, Text } from "react-konva";
import useResizeObserver from "use-resize-observer";

const CATEGORICAL_COLORS = [
  "#d32f2f", // red
  "#1976d2", // blue
  "##388e3c", // green
  "#fbc02d", // yellow
  "#455a64", // bluegray
  "#c2185b", // pink
  "#7b1fa2", // purple
  "#e64a19", // orange
  "#00796b" // teal
];

const LiveStreamContainer = styled.div`
  position: absolute;
  top: 0;
  z-index: 10;
  background-color: black;

  transition: all 0.5s;
  ${props =>
    props.fullscreen
      ? css`
          left: 0;
          right: 0;
          bottom: 0;
        `
      : css`
          left: 25vw;
          right: 50vw;
          bottom: 70vh;
        `}
`;

const FullscreenButton = styled.button`
  position: absolute;
  bottom: 0;
  right: 0;
  background-color: transparent;
  border: none;
  color: white;
  cursor: pointer;
  z-index: 20;
`;

const RecordButton = styled.button`
  position: absolute;
  top: 5px;
  right: 0;
  background-color: transparent;
  border: none;
  color: red;
  cursor: pointer;
  z-index: 20;
`;

const LiveStreamErrorMessage = styled.p`
  position: absolute;
  bottom: 0;
  left: 0;
  color: white;
  margin: 4px;
  font-family: Tahoma, Verdana, Segoe, sans-serif;
  font-size: 10px;
`;

const linkPlayer = (
  api,
  [reactRef, width, height] = useResizeObserver(),
  [streamResolution, setStreamResolution] = useState(null),
  [connected, setConnected] = useState(false)
) => {
  useEffect(() => {
    if (!connected) {
      const canvas = reactRef.current;
      // const player = new WSAvcPlayer(canvas, "webgl", 1, 35);
      // player.connect(api.getLiveStreamUrl());
      // player.on("initalized", e => {
      //   player.on("frame_shift", () =>
      //     setStreamResolution({ width: e.width, height: e.height })
      //   );
      // });
      setConnected(true);
    }
  });

  return { reactRef, width, height, streamResolution };
};

const linkRecorder = (
  api,
  [recording, setRecording] = useState(false)
): [boolean, Dispatch<SetStateAction<boolean>>] => [
  recording,
  (recording: boolean) => {
    api.setRecording(recording);
    setRecording(recording);
  }
];

const linkVisionSystem = (
  api,
  [visionResults, setVisionResults] = useState(null)
) =>
  visionResults === null
    ? api.onVisionSystemResult(setVisionResults) || {}
    : visionResults;

const LiveStream = ({
  api,
  _playerState: { reactRef, width, height, streamResolution } = linkPlayer(
    api
  ) as any,
  _visionState: visionResults = linkVisionSystem(api),
  _fullscreenState: [fullscreen, setFullscreen] = useState(false),
  _recordingState: [recording, setRecording] = linkRecorder(api)
}) => (
  <LiveStreamContainer fullscreen={fullscreen}>
    <FullscreenButton onClick={() => setFullscreen(!fullscreen)}>
      <FontAwesomeIcon icon={faExpand} />
    </FullscreenButton>
    <RecordButton onClick={() => setRecording(!recording)}>
      {recording ? (
        <FontAwesomeIcon icon={faStopCircle} />
      ) : (
        <FontAwesomeIcon icon={faPlayCircle} />
      )}{" "}
      <span style={{ color: "white" }}>REC</span>
    </RecordButton>

    {streamResolution ? (
      ((ctr = 0) => (
        <Stage
          width={width}
          height={height}
          style={{
            top: 0,
            right: 0,
            bottom: 0,
            left: 0,
            position: "absolute"
          }}
        >
          <Layer>
            {Object.keys(visionResults).map(
              (objName, colorIdx, _, color = CATEGORICAL_COLORS[colorIdx]) =>
                visionResults[objName].map(
                  (
                    [[[x1, y1], [x2, y2]], bearing, distance],
                    _idx,
                    _arr,
                    rescale = streamResolution
                      ? rescaler(streamResolution, { width, height })
                      : x => x
                  ) => {
                    if (width === 1 && height === 1) {
                      return null;
                    }
                    const res = (
                      <Fragment key={ctr}>
                        <Rect
                          x={rescale(x1, true)}
                          y={rescale(streamResolution.height - y2, false)}
                          width={rescale(x2 - x1, true)}
                          height={rescale(y2 - y1, false)}
                          stroke={color}
                          strokeWidth={1}
                        />
                        {fullscreen ? (
                          <Text
                            x={rescale(x1 + 2, true)}
                            y={rescale(streamResolution.height - y2 + 2, false)}
                            fill={color}
                            text={`${objName}: ${distance}cm@${bearing}°`}
                          />
                        ) : null}
                      </Fragment>
                    );
                    console.log("got res", res);
                    ctr += 1;
                    return res;
                  }
                )
            )}
          </Layer>
        </Stage>
      ))()
    ) : (
      <LiveStreamErrorMessage>LOADING</LiveStreamErrorMessage>
    )}

    <canvas ref={reactRef} style={{ width: "100%", height: "100%" }} />
  </LiveStreamContainer>
);

const rescaler = (
  { width: stream_width, height: stream_height },
  { width, height }
) => (val, is_x_dir) => {
  console.log("rescaling ", val, "is_x_dir", is_x_dir);
  console.log("stream resolution", stream_width, stream_height);
  console.log("curr resolution", width, height);
  const res = is_x_dir
    ? (val * width) / stream_width
    : (val * height) / stream_height;
  console.log("rescale result:", res);
  return res;
};

export const ManagedStream = ({ api = useApi() }) =>
  api ? <LiveStream api={api} /> : null;

export default LiveStream;
