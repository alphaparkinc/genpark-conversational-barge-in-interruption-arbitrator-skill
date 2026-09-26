import sys, json
from client import ConversationalBargeInArbitrator

def main():
    print("Testing ConversationalBargeInArbitrator...")
    arb = ConversationalBargeInArbitrator()
    res = arb.run_benchmark_barge_in_arbitration()
    print(json.dumps(res, indent=2))
    assert res["echo_decision"] == "SUPPRESS_ACOUSTIC_ECHO"
    assert res["backchannel_decision"] == "ACKNOWLEDGE_BACKCHANNEL"
    assert res["barge_in_decision"] == "EXECUTE_BARGE_IN"
    print("All Conversational Barge-In Arbitrator tests passed successfully!")

if __name__ == "__main__":
    main()
