package com.mycompany.myapp.delegate;

import com.mycompany.myapp.service.dto.FriendlyShoulderProcessDTO;
import org.camunda.bpm.engine.delegate.DelegateExecution;
import org.camunda.bpm.engine.delegate.JavaDelegate;
import org.springframework.stereotype.Component;

@Component
public class LogResponseDelegate implements JavaDelegate {

    @Override
    public void execute(DelegateExecution delegateExecution) throws Exception {

        FriendlyShoulderProcessDTO pi = (FriendlyShoulderProcessDTO) delegateExecution.getVariable("pi");

        String description = pi.getFriendlyShoulder().getDescription();

        System.out.println("\n\n\n#####################################################");
        System.out.println("#####################################################");
        System.out.println("#####################################################");
        System.out.println("################ LOGGING DESCRIPTION ################");
        System.out.println(description);
        System.out.println("#####################################################");
        System.out.println("#####################################################");
        System.out.println("#####################################################\n\n\n");
    }
}