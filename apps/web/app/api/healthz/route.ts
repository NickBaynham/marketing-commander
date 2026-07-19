// Health route for container and bootstrap checks (REQ-048, AC-001).
export async function GET() {
  return Response.json({ status: "ok" });
}
