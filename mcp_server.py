import sys, json
from client import ConversationalBargeInArbitrator

def main():
    arb = ConversationalBargeInArbitrator()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps(arb.run_benchmark_barge_in_arbitration(), indent=2))
        return

    for line in sys.stdin:
        if not line.strip(): continue
        try:
            req = json.loads(line)
            method = req.get("method")
            params = req.get("params", {})
            rid = req.get("id")

            if method == "tools/list":
                res = {
                    "tools": [
                        {"name": "evaluate_interruption_event", "description": "Arbitrate whether an incoming speech event is a true barge-in, backchannel, or echo."},
                        {"name": "compute_playback_rollback_state", "description": "Calculate exact token/character rollback for interrupted agent speech."},
                        {"name": "classify_utterance_intent", "description": "Classify user speech snippet into confirmation vs intent redirect."},
                        {"name": "run_benchmark_barge_in_arbitration", "description": "Run comprehensive barge-in test scenarios."}
                    ]
                }
            elif method == "tools/call":
                tname = params.get("name")
                args = params.get("arguments", {})
                if tname == "evaluate_interruption_event":
                    out = arb.evaluate_interruption_event(
                        args.get("agent_is_speaking", True),
                        args.get("incoming_audio_energy_db", -20.0),
                        args.get("incoming_transcript", ""),
                        args.get("echo_correlation_score", 0.0),
                        args.get("utterance_duration_ms", 300)
                    )
                elif tname == "compute_playback_rollback_state":
                    out = arb.compute_playback_rollback_state(args.get("full_agent_script", ""), args.get("playback_progress_ratio", 0.5))
                elif tname == "classify_utterance_intent":
                    out = arb.classify_utterance_intent(args.get("user_transcript_snippet", ""))
                elif tname == "run_benchmark_barge_in_arbitration":
                    out = arb.run_benchmark_barge_in_arbitration()
                else:
                    out = {"error": f"Unknown tool {tname}"}
                res = {"content": [{"type": "text", "text": json.dumps(out)}]}
            else:
                res = {"error": "Unsupported method"}
            print(json.dumps({"jsonrpc": "2.0", "id": rid, "result": res}), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "error": {"code": -32603, "message": str(e)}}), flush=True)

if __name__ == "__main__":
    main()
