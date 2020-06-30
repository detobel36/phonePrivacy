package be.ulb.testbed;

import android.widget.ProgressBar;

/**
 * Store test action
 */
public abstract class TestAction {

    private static TestActivity main = TestActivity.getMainInstance();

    private final ProgressBar progressBar;

    public TestAction(final int layoutId) {
        progressBar = main.findViewById(layoutId);
    }

    public ProgressBar getProgressBar() {
        return progressBar;
    }

    public abstract void executeAction();

}
