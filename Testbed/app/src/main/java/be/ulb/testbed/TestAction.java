package be.ulb.testbed;

import android.widget.ProgressBar;

import androidx.appcompat.app.AppCompatActivity;

/**
 * Store test action
 */
public abstract class TestAction {

    private final ProgressBar progressBar;
    private final int timer;

    protected TestAction(final AppCompatActivity testView, final int layoutId, final int timer) {
        progressBar = testView.findViewById(layoutId);
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
