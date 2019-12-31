#!/bin/sh

set -o errexit

FILENAME=$(basename $0)
DEBUG="true" ## if true, verbose debug output is activated
DEBUG="false"


errorexit()
{
    debugthis "function myexit($1) called"

    [ "$1" -lt 1 ] && echo "$FILENAME done."
    if [ "$1" -gt 0 ]; then
        echo
        echo "$FILENAME aborted with errorcode $1:  $2"
        echo
        #echo "See \"${LOGFILE}\" for further details."
        #echo
    fi

    exit $1
}


debugthis()
{
        [ "${DEBUG}" = "true" ] && echo $FILENAME: DEBUG: $@
        #echo $FILENAME: DEBUG: $@ >> ${LOGFILE}
        echo "do nothing" >/dev/null
}


reportbig()
{
    echo "\n----------------------------------------------------------------"
    echo "$FILENAME: ${@}"
    echo "----------------------------------------------------------------\n"
    #echo $FILENAME: $@ >> ${LOGFILE}
}


report()
{
    echo "$FILENAME: ${@}"
    #echo $FILENAME: $@ >> ${LOGFILE}
}


handle_comparison()
{
    testdir="${1}"
    expoutput="${2}"

    number=$(echo "${expoutput}" | sed 's/expected_output//' | sed 's/\..*//')
    debugthis "test number: [${number}]"

    num_outputs=$(ls -1 output${number}.* | wc -l)
    debugthis "num_outputs: [$num_outputs]"
    [ $num_outputs -eq 1 ] || errorexit 10 "Test result ${number} of \"${testdir}\" failed: missing output file!"

    diff "${expoutput}" output${number}.* || errorexit 15 "Test result ${number} of \"${testdir}\" failed: output differs from expected output!"
}


handle_testcase()
{
    testdir="${1}"

    cd "${testdir}"
    report "handling test-case: \"${testdir}\""

    debugthis "removing old output files"
    rm -f output*

    debugthis "calling \"runtest.sh\""
    . ./runtest.sh

    debugthis "comparing results"
    for expoutput in expected_output*; do
	handle_comparison "${testdir}" "${expoutput}"
    done

    debugthis "switching back to original directory"
    cd ..
    echo
}


report "starting a test-run for all test cases ..."
echo
for testdir in test_*; do
    handle_testcase "${testdir}"
done
reportbig "all test cases finished successfully."

#end
