package be.ulb.testbed;

import android.widget.ProgressBar;

import androidx.appcompat.app.AppCompatActivity;

/**
 * Store test action
 */
public abstract class TestAction {

    private final ProgressBar progressBar;

    protected TestAction(final AppCompatActivity testView, final int layoutId) {
        progressBar = testView.findViewById(layoutId);
    }

    public ProgressBar getProgressBar() {
        return progressBar;
    }

    public abstract void executeAction();

}
