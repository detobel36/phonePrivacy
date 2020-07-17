package be.ulb.testbed;

import android.app.Activity;
import android.widget.ProgressBar;

/**
 * Store test action
 */
public abstract class TestAction {

    private final ProgressBar progressBar;
    private final int timer;

    protected TestAction(final Activity testView, final int layoutId, final int timer) {
        progressBar = (ProgressBar) testView.findViewById(layoutId);
        this.timer = timer;
    }

    public ProgressBar getProgressBar() {
        return progressBar;
    }

    /**
     * Get the timing durint this task execute
     *
     * @return the time in second
     */
    public int getTimer() {
        return timer;
    }

    public abstract void executeAction();

}
