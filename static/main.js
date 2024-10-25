document.addEventListener('DOMContentLoaded', (event) => {
    mainInit();  // 페이지가 완전히 로드된 후 mainInit 호출
});

let captureInProgress = false;  // 중복 요청 방지 플래그

function captureImage() {
    if (captureInProgress) return;  // 중복 요청 방지

    captureInProgress = true;  // 요청 중임을 표시
    var cameraView = document.getElementById("cameraview");
    var canvas = document.getElementById("canvas");
    var context = canvas.getContext("2d");

    // 비디오 프레임을 캔버스에 그리기
    context.drawImage(cameraView, 0, 0, canvas.width, canvas.height);

    // 캔버스를 Blob으로 변환하고 서버로 전송
    canvas.toBlob(function(blob) {
        var formData = new FormData();
        formData.append("file", blob, "captured_image.png");

        // 서버로 이미지 분석 요청
        fetch('http://localhost:8000/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (response.redirected) {
                // 리디렉션이 발생했을 때, 해당 URL로 이동
                window.location.href = response.url;
            } else {
                return response.json();
            }
        })
        .then(data => {
            console.log('Server response:', data);  // 서버 응답을 로그로 출력
        })
        .catch(error => {
            console.error('Error analyzing image:', error);
        })
        .finally(() => {
            captureInProgress = false;  // 요청이 끝나면 플래그 리셋
        });
    }, 'image/png');
}

function mainInit() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        alert("Media Device not supported");
        return;
    }

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            var cameraView = document.getElementById("cameraview");
            cameraView.srcObject = stream;
        })
        .catch(error => console.error("Error accessing camera:", error));

    var captureButton = document.getElementById("captureButton");
    if (captureButton) {
        captureButton.addEventListener("click", captureImage);  // 이벤트 리스너 추가
    }
}
