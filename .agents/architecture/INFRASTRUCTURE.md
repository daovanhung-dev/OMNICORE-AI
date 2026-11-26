# Hạ tầng — khảo sát theo repository thực

- Phát hiện manifest/scripts/Docker/compose/Kubernetes/CI nếu **có thật**.
- Ghi topology, reverse proxy/TLS, deployment environment, secrets store, probes/logging/metrics.
- Không áp server IP, domain, database type hoặc provider của dự án khác.
- Không tự deploy, chỉnh firewall, sửa production data khi không được giao và chấp thuận.
- Mọi báo cáo rõ local test / staging test / production verified; không đánh đồng.
